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
    # Have my doubts if root mount point + path actually work in path function
    xfce_installed = Path("root_mount_point + /usr/share/xsessions/xfce.desktop")
    # cleaning stuff from cleaner script may be needed
    # config copied before creating new user, so use skel folder
    COPY_CMD = "cp -f"
    SKEL_CONFIG = "/etc/skel/.config/xfce"
        try:
            if xfce_installed.exists():
                    subprocess.call(COPY_CMD.split(' ') + [SKEL_CONFIG] + [root_mount_point + SKEL_CONFIG])
        except:
            pass
