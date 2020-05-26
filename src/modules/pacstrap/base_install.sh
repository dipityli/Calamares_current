#!/bin/bash

_make_pacstrap_calamares(){

rm -rf /usr/bin/pacstrap_calamares # temporary untill pacstrap_calamares is removed from github
sed -e '/chroot_add_mount proc/d' -e '/chroot_add_mount sys/d' -e '/ignore_error chroot_maybe_add_mount/d' -e '/chroot_add_mount udev/d' -e '/chroot_add_mount devpts/d' -e '/chroot_add_mount shm/d' -e '/chroot_add_mount \/run/d' -e '/chroot_add_mount tmp/d' -e '/efivarfs \"/d' /usr/bin/pacstrap >/usr/bin/pacstrap_calamares
chmod +x /usr/bin/pacstrap_calamares

}

_keyserver(){

TIME="time_servers.log"
if [ ! -d rank ]; then mkdir rank; fi
cd rank

servers_array=(
"keys.openpgp.org"
"pgp.mit.edu"
"keyring.debian.org"
"keyserver.ubuntu.com"
"zimmermann.mayfirst.org"
"pool.sks-keyservers.net"
"na.pool.sks-keyservers.net"
"eu.pool.sks-keyservers.net"
"oc.pool.sks-keyservers.net"
"p80.pool.sks-keyservers.net"
"ipv4.pool.sks-keyservers.net"
"ipv6.pool.sks-keyservers.net"
"subset.pool.sks-keyservers.net"
)

rm -rf $TIME.* 
for server in "${servers_array[@]}"
do
    ping -c 1 $server 2>&1 > $TIME.$server
done

rm -rf $(grep -r "100% packet loss" * |awk '{ print $1 }' | sed 's/:.*//g')

# Unfortunately sometimes generates some type of server door like 2001:470:1:116::6 and pacman-key doesn't work, so need to get the original url again :(
RANK_BEST=$(grep "time=" * | sort -k8 --version-sort | uniq -u | head -n 1 | awk '{ print $4 }')

FINAL=$(grep -n "$RANK_BEST" * |grep "PING" |sed s'/^.*PING //' |sed s'/(.*//')

pacman-key --refresh-keys --keyserver $FINAL

}

_update_db(){

# Update database step by step
# For iso only
# Necessary for old ISOs

haveged -w 1024
pacman-key --init
pkill haveged
pacman-key --populate
_keyserver
cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.bak

RANK_MIRRORS="/usr/bin/update-mirrorlist"
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

# Stored all commands as strings, hope it helps beginners
_chroot_path=$(cat /tmp/chrootpath.txt) # this can't be stored as string, sorry beginners :)

_pacstrap="/usr/bin/pacstrap_calamares -c" # make a sed config later

_rsync="rsync -vaRI" # would cp command be less processor consuming or easier for beginners?
#CHROOT_CLEANER_SCRIPT="/usr/bin/chrooted_cleaner_script.sh"
#CLEANER_SCRIPT="/usr/bin/cleaner_script.sh"
_install_scripts="/usr/bin/{chrooted_cleaner_script,cleaner_script}.sh"
_pacman_conf="/etc/pacman.conf"
_pacman_mirrors="/etc/pacman.d/mirrorlist"

for pkgs in "${_packages_array[*]}" "${_oldbase_array[*]}" "${_filesystem_array[*]}"
do $_pacstrap $_chroot_path $pkgs
    
done

#$_pacstrap $_chroot_path "${_packages_array[*]}" "${_oldbase_array[*]}" "${_filesystem_array[*]}"

#$RSYNC_CMD $CHROOT_CLEANER_SCRIPT /tmp/$_chroot_path
#$RSYNC_CMD $CLEANER_SCRIPT /tmp/$_chroot_path
# do in a single shot later unless is hard for beginners to understand
$_rsync $_install_scripts $_chroot_path
$_rsync $_pacman_conf $_chroot_path
$_rsync $_pacman_mirrors $_chroot_path
$_rsync "/tmp/run_once" $_chroot_path

}

############ SCRIPT STARTS HERE ############
_make_pacstrap_calamares
_run
############ SCRIPT ENDS HERE ##############
