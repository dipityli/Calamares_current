#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Made by fernandomaroto for EndeavourOS and Portergos.
# Should work in any arch-based distros
# Trying K.I.S.S filosophy
# Detect XFCE4 DE netinstall

#################################################################
# PROTOTYPE
#################################################################

import subprocess
import libcalamares
from pathlib import Path

root_mount_point = libcalamares.globalstorage.value("rootMountPoint")


xfce_installed = Path("root_mount_point + /usr/share/xsessions/xfce.desktop")

    try:
        if not xfce_installed.exists():
            subprocess.call(???????.split(' '))
    except:
        pass

    COPY_CMD = "cp -f"
    DEST_ETC = "/etc"

    subprocess.call(COPY_CMD.split(' ') + [PACMAN_CONF] + [root_mount_point + DEST_ETC])

    subprocess.call(COPY_CMD.split(' ') + ["/tmp/run_once"] + [root_mount_point + "/tmp/run_once"])
