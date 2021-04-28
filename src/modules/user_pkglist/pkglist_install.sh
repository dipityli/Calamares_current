#!/bin/bash

Main() {
    local _pkglist="/home/liveuser/user_pkglist.txt"
    local pkgs _chroot_path

    if [ -f "$_pkglist" ] ; then
        pkgs=$(echo $(cat $_pkglist | sed 's|#.*||'))  # echo removes white spaces
        if [ -n "$pkgs" ] ; then
            _chroot_path=$(cat /tmp/chrootpath.txt)
            pacman -Sy --noconfirm --needed --root $_chroot_path $pkgs
        fi
    fi
}

Main
