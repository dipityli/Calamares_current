#!/bin/bash

_make_pacstrap_calamares(){

if [ ! -f "/usr/local/bin/pacstrap_calamares" ]

then

sed -e '/chroot_add_mount proc/d' -e '/chroot_add_mount sys/d' -e '/ignore_error chroot_maybe_add_mount/d' -e '/chroot_add_mount udev/d' -e '/chroot_add_mount devpts/d' -e '/chroot_add_mount shm/d' -e '/chroot_add_mount \/run/d' -e '/chroot_add_mount tmp/d' -e '/efivarfs \"/d' /usr/bin/pacstrap >/usr/bin/pacstrap_calamares
chmod +x /usr/local/bin/pacstrap_calamares

fi

}

_update_db(){

# Update database step by step
# For iso only
# Necessary for old ISOs

haveged -w 1024
pacman-key --init
pkill haveged
pacman-key --populate
cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.bak

RANK_MIRRORS="/usr/local/bin/update-mirrorlist"
BEST_MIRRORS="reflector --verbose -a1 -f10 -l70 -phttps --sort rate --save /etc/pacman.d/mirrorlist"

if [ -f $RANK_MIRRORS ]
then
    $RANK_MIRRORS
else
    $BEST_MIRRORS
fi

# After above no need to run cmds again when launch calamares a second time
touch /tmp/run_once
   
}

_run(){

if [ ! -f "/tmp/run_once" ]
then
    _update_db
fi
  
# Install base system + endeavouros packages + copy necessary config files

_packages_array=( base sudo grub endeavouros-keyring endeavouros-mirrorlist grub2-theme-endeavouros xterm )

_oldbase_array=( mkinitcpio mkinitcpio-busybox mkinitcpio-nfs-utils diffutils inetutils jfsutils less logrotate man-db man-pages mdadm nano netctl perl s-nail sysfsutils systemd-sysvcompat texinfo usbutils vi which linux linux-firmware device-mapper )

_filesystem_array=( cryptsetup e2fsprogs f2fs-tools btrfs-progs lvm2 reiserfsprogs xfsprogs )

_chroot_path=$(cat /tmp/chrootpath.txt) # can't be stored as string

_pacstrap="/usr/local/bin/pacstrap_calamares -c"

for pkgs in "${_packages_array[*]}" "${_oldbase_array[*]}" "${_filesystem_array[*]}"
do
    $_pacstrap -c $_chroot_path $pkgs
done

_files_to_copy=(

/usr/local/bin/{chrooted_cleaner_script,cleaner_script}.sh
/etc/pacman.conf
/etc/pacman.d/mirrorlist
/tmp/run_once
/etc/default/grub

)

for copy_files in "${_files_to_copy[@]}"
do
    rsync -vaRI $copy_files $_chroot_path
done

}

############ SCRIPT STARTS HERE ############
_make_pacstrap_calamares
_run
############ SCRIPT ENDS HERE ##############
