#!/bin/bash

_pkglist="/home/liveuser/user_pkglist.txt"

if [ -f "$_pkglist" ]

then
    
    _chroot_path=$(cat /tmp/chrootpath.txt)

    for pkgs in $(cat $_pkglist | grep -v '^[ ]*#')
    do
        pacman -Sy $pkgs --noconfirm --needed --root $_chroot_path
    done
fi
