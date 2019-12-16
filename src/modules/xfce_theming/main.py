#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Made by fernandomaroto for EndeavourOS and Portergos.
# Should work in any arch-based distros
# Trying K.I.S.S filosophy
# Detect XFCE4 DE netinstall

import subprocess
import libcalamares
from pathlib import Path

root_mount_point = libcalamares.globalstorage.value("rootMountPoint")

def run():
    # Checks if xfce was installed in the system
    xfce_installed = Path(root_mount_point + "/usr/share/xsessions/xfce.desktop")
    RSYNC_CMD = "rsync -vaRI"
    SKEL_CONFIG = "/etc/skel/.config/xfce4"
    # New version is needed, from now on we'll have a package to install backgrounds to all DEs
    SYMLINK_ORIG = "ln -sf /usr/share/endeavouros/backgrounds/endeavouros-wallpaper.png"
    #SYMLINK_ORIG = "ln -sf /usr/share/endeavouros/endeavouros-wallpaper.png"
    SYMLINK_FIRST = "/usr/share/backgrounds/xfce/xfce-stripes.png"
    SYMLINK_SECOND = "/usr/share/backgrounds/xfce/xfce-teal.jpg"
    BACKGROUNG_IMG = "/usr/share/endeavouros/backgrounds/endeavouros-wallpaper.png"
    LIGHTDM_CONFIG = "/etc/lightdm/"
    try:
        if xfce_installed.exists():
            subprocess.call(SYMLINK_ORIG.split(' ') + [root_mount_point + SYMLINK_FIRST])
            subprocess.call(SYMLINK_ORIG.split(' ') + [root_mount_point + SYMLINK_SECOND])
            subprocess.call(RSYNC_CMD.split(' ') + [SKEL_CONFIG] + [root_mount_point])
            subprocess.call(RSYNC_CMD.split(' ') + [BACKGROUNG_IMG] + [root_mount_point])
            subprocess.call(RSYNC_CMD.split(' ') + [LIGHTDM_CONFIG] + [root_mount_point])


    except:
        pass
