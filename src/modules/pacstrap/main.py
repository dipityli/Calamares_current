#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Originally was unpackpfs module
# Changed by Fernando "maroto" for EndeavourOS to add pacstrap function for online install
# Updates all keyrings, populate etc

import os
import re
import shutil
import subprocess
import sys
import tempfile
#import requests

from pathlib import Path
from libcalamares import *

import gettext
_ = gettext.translation("calamares-python",
                        localedir=utils.gettext_path(),
                        languages=utils.gettext_languages(),
                        fallback=True).gettext

def pretty_name():
    return _("Filling up filesystems.")


class UnpackEntry:
    """
    Extraction routine using rsync.

    :param source:
    :param sourcefs:
    :param destination:
    """
    __slots__ = ['source', 'sourcefs', 'destination', 'copied', 'total']

    def __init__(self, source, sourcefs, destination):
        self.source = source
        self.sourcefs = sourcefs
        self.destination = destination
        self.copied = 0
        self.total = 0


ON_POSIX = 'posix' in sys.builtin_module_names


def list_excludes(destination):
    """
    List excludes for rsync.

    :param destination:
    :return:
    """
    lst = []
    extra_mounts = globalstorage.value("extraMounts")
    if extra_mounts is None:
        extra_mounts = []

    for extra_mount in extra_mounts:
        mount_point = extra_mount["mountPoint"]

        if mount_point:
            lst.extend(['--exclude', mount_point + '/'])

    return lst


def file_copy(source, dest, progress_cb):
    """
    Extract given image using rsync.

    :param source:
    :param dest:
    :param progress_cb:
    :return:
    """
    # Environment used for executing rsync properly
    # Setting locale to C (fix issue with tr_TR locale)
    at_env = os.environ
    at_env["LC_ALL"] = "C"

    # `source` *must* end with '/' otherwise a directory named after the source
    # will be created in `dest`: ie if `source` is "/foo/bar" and `dest` is
    # "/dest", then files will be copied in "/dest/bar".
    if not source.endswith("/"):
        source += "/"

    num_files_copied = 0  # Gets updated through rsync output

    args = ['rsync', '-aHAXr']
    args.extend(list_excludes(dest))
    args.extend(['--progress', source, dest])
    process = subprocess.Popen(
        args, env=at_env, bufsize=1, stdout=subprocess.PIPE, close_fds=ON_POSIX
        )

    for line in iter(process.stdout.readline, b''):
        # rsync outputs progress in parentheses. Each line will have an
        # xfer and a chk item (either ir-chk or to-chk) as follows:
        #
        # - xfer#x => Interpret it as 'file copy try no. x'
        # - ir-chk=x/y, where:
        #     - x = number of files yet to be checked
        #     - y = currently calculated total number of files.
        # - to-chk=x/y, which is similar and happens once the ir-chk
        #   phase (collecting total files) is over.
        #
        # If you're copying directory with some links in it, the xfer#
        # might not be a reliable counter (for one increase of xfer, many
        # files may be created).
        m = re.findall(r'xfr#(\d+), ..-chk=(\d+)/(\d+)', line.decode())

        if m:
            # we've got a percentage update
            num_files_remaining = int(m[0][1])
            num_files_total_local = int(m[0][2])
            # adjusting the offset so that progressbar can be continuesly drawn
            num_files_copied = num_files_total_local - num_files_remaining

            # I guess we're updating every 100 files...
            if num_files_copied % 100 == 0:
                progress_cb(num_files_copied, num_files_total_local)

    process.wait()
    progress_cb(num_files_copied, num_files_total_local)  # Push towards 100%

    # 23 is the return code rsync returns if it cannot write extended
    # attributes (with -X) because the target file system does not support it,
    # e.g., the FAT EFI system partition. We need -X because distributions
    # using file system capabilities and/or SELinux require the extended
    # attributes. But distributions using SELinux may also have SELinux labels
    # set on files under /boot/efi, and rsync complains about those. The only
    # clean way would be to split the rsync into one with -X and
    # --exclude /boot/efi and a separate one without -X for /boot/efi, but only
    # if /boot/efi is actually an EFI system partition. For now, this hack will
    # have to do. See also:
    # https://bugzilla.redhat.com/show_bug.cgi?id=868755#c50
    # for the same issue in Anaconda, which uses a similar workaround.
    if process.returncode != 0 and process.returncode != 23:
        utils.warning("rsync failed with error code {}.".format(process.returncode))
        return _("rsync failed with error code {}.").format(process.returncode)

    return None


class UnpackOperation:
    """
    Extraction routine using unsquashfs.

    :param entries:
    """

    def __init__(self, entries):
        self.entries = entries
        self.entry_for_source = dict((x.source, x) for x in self.entries)

    def report_progress(self):
        """
        Pass progress to user interface
        """
        progress = float(0)

        done = 0
        total = 0
        complete = 0
        for entry in self.entries:
            if entry.total == 0:
                continue
            total += entry.total
            done += entry.copied
            if entry.total == entry.copied:
                complete += 1

        if done > 0 and total > 0:
            progress = 0.05 + (0.90 * done / total) + (0.05 * complete / len(self.entries))

        job.setprogress(progress)

    def run(self):
        """
        Extract given image using unsquashfs.

        :return:
        """
        source_mount_path = tempfile.mkdtemp()

        try:
            for entry in self.entries:
                imgbasename = os.path.splitext(
                    os.path.basename(entry.source))[0]
                imgmountdir = os.path.join(source_mount_path, imgbasename)
                os.mkdir(imgmountdir)

                self.mount_image(entry, imgmountdir)

                fslist = ""

                if entry.sourcefs == "squashfs":
                    if shutil.which("unsquashfs") is None:
                        utils.warning("Failed to find unsquashfs")

                        return (_("Failed to unpack image \"{}\"").format(entry.source),
                                _("Failed to find unsquashfs, make sure you have the squashfs-tools package installed"))

                    fslist = subprocess.check_output(
                        ["unsquashfs", "-l", entry.source]
                        )

                if entry.sourcefs == "ext4":
                    fslist = subprocess.check_output(
                        ["find", imgmountdir, "-type", "f"]
                        )

                entry.total = len(fslist.splitlines())

                self.report_progress()
                error_msg = self.unpack_image(entry, imgmountdir)

                if error_msg:
                    return (_("Failed to unpack image \"{}\"").format(entry.source),
                            error_msg)

            return None
        finally:
            shutil.rmtree(source_mount_path, ignore_errors=True, onerror=None)

    def mount_image(self, entry, imgmountdir):
        """
        Mount given image as loop device.

        :param entry:
        :param imgmountdir:
        """
        if os.path.isdir(entry.source):
            subprocess.check_call(["mount",
                                   "--bind", entry.source,
                                   imgmountdir])
        elif os.path.isfile(entry.source):
            subprocess.check_call(["mount",
                                   entry.source,
                                   imgmountdir,
                                   "-t", entry.sourcefs,
                                   "-o", "loop"
                                   ])
        else: # entry.source is a device
            subprocess.check_call(["mount",
                                   entry.source,
                                   imgmountdir,
                                   "-t", entry.sourcefs
                                   ])

    def unpack_image(self, entry, imgmountdir):
        """
        Unpacks image.

        :param entry:
        :param imgmountdir:
        :return:
        """
        def progress_cb(copied, total):
            """ Copies file to given destination target.

            :param copied:
            """
            entry.copied = copied
            if total > entry.total:
                entry.total = total
            self.report_progress()

        try:
            return file_copy(imgmountdir, entry.destination, progress_cb)
        finally:
            subprocess.check_call(["umount", "-l", imgmountdir])


def get_supported_filesystems():
    """
    Reads /proc/filesystems (the list of supported filesystems
    for the current kernel) and returns a list of (names of)
    those filesystems.
    """
    PATH_PROCFS = '/proc/filesystems'

    if os.path.isfile(PATH_PROCFS) and os.access(PATH_PROCFS, os.R_OK):
        with open(PATH_PROCFS, 'r') as procfile:
            filesystems = procfile.read()
            filesystems = filesystems.replace(
                "nodev", "").replace("\t", "").splitlines()
            return filesystems

    return []

def update_db():

    # Hope is simpler this way

    START_HAVEGED = "haveged -w 1024"
    PACMAN_INIT = "pacman-key --init"
    PACMAN_POPULATE = "pacman-key --populate"
    PACMAN_REFRESH ="pacman-key --refresh-keys"
    STOP_HAVEGED = "pkill haveged"
    BACKUP_MIRROLIST = "cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.bak"
    BEST_MIRRORS = "reflector --verbose --age 8 --fastest 128 --latest 64 --number 32 --sort rate --save /etc/pacman.d/mirrorlist"

    # Update database, step by step in the running iso only. Necessary if running old iso version
    subprocess.call(START_HAVEGED.split(' ')) 
    subprocess.call(PACMAN_INIT.split(' '))  
    subprocess.call(PACMAN_POPULATE.split(' ')) 
    subprocess.call(PACMAN_REFRESH.split(' '))
    subprocess.call(STOP_HAVEGED.split(' '))   

    # Commands above give us more control and remove the need to use packages module to update db and system.
    # update_db: false
    # update_system: false
    # Speed up download using fastest mirrors

    subprocess.call(BACKUP_MIRROLIST.split(' '))  
    subprocess.call(BEST_MIRRORS.split(' '))

    # After the above there is no need to run cmds again in case the user tries to launch calamares a second time

    try:
        open('/tmp/run_once', 'a')
        run_once.close()
    except:
        pass
    
def run():
    """
    Install base filesystem.
    """
    root_mount_point = globalstorage.value("rootMountPoint")

    # created new function above to update, populate, refresh, best mirrors etc
    
    executed_before = Path("/tmp/run_once")

    try:
        if not executed_before.exists():
            update_db()
    except:
        pass

    # Install base system + endeavouros packages + copy necessary config files

    PACSTRAP = "/usr/bin/pacstrap_endeavouros -c"
    PACKAGES = "base sudo grub endeavouros-keyring endeavouros-mirrorlist grub2-theme-endeavouros"
    COPY_CMD = "cp -f"
    CLEANER_SCRIPT = "/usr/bin/cleaner_script.sh"
    PACMAN_CONF = "/etc/pacman.conf"
    PACMAN_MIRRORS = "/etc/pacman.d/mirrorlist"
    OS_RELEASE = "/etc/os-release"
    DEST_BIN = "/usr/bin"
    DEST_ETC = "/etc"
    DEST_MIRRORS = "/etc/pacman.d"
    GRUB_CONF = "/etc/default/grub"
    DEST_GRUB = "/etc/default"

    subprocess.call(PACSTRAP.split(' ') + [root_mount_point] + PACKAGES.split(' '))

    subprocess.call(COPY_CMD.split(' ') + [CLEANER_SCRIPT] + [root_mount_point + DEST_BIN])

    subprocess.call(COPY_CMD.split(' ') + [PACMAN_CONF] + [root_mount_point + DEST_ETC])

    subprocess.call(COPY_CMD.split(' ') + [OS_RELEASE] + [root_mount_point + DEST_ETC])

    subprocess.call(COPY_CMD.split(' ') + [GRUB_CONF] + [root_mount_point + DEST_GRUB])

    subprocess.call(COPY_CMD.split(' ') + [PACMAN_MIRRORS] + [root_mount_point + DEST_MIRRORS])
