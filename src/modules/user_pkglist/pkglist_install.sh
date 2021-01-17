#!/bin/bash

_pkglist="/home/liveuser/user_pkglist.txt"

if [ -f "$_pkglist" ]

then
    # Need to add module to calamares at some new module
    
    _pacstrap="/usr/bin/pacstrap_calamares -c"
    _chroot_path=$(cat /tmp/chrootpath.txt)

    for pkgs in $(cat $_pkglist)
    do
        _pacstrap -c $_chroot_path $pkgs
        # or use pacman - executed from live environment
        # pacman -S $pkgs --noconfirm --needed --root $_chroot_path
    done
fi
