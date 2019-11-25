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
    RSYNC_CMD = "rsync -vaR"
    SKEL_CONFIG = "/etc/skel/.config/xfce4"
    BACKGROUNG_IMG = "/usr/share/endeavouros/endeavouros-wallpaper.png"
    LIGHTDM_CONFIG = "/etc/lightdm/"
    try:
        if xfce_installed.exists():
            subprocess.call(RSYNC_CMD.split(' ') + [SKEL_CONFIG] + [root_mount_point])
            subprocess.call(RSYNC_CMD.split(' ') + [BACKGROUNG_IMG] + [root_mount_point])
            subprocess.call(RSYNC_CMD.split(' ') + [LIGHTDM_CONFIG] + [root_mount_point])

    except:
        pass
