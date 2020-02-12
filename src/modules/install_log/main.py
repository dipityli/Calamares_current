#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Made by fernandomaroto for EndeavourOS and Portergos.
# Simply copy install log from live environment to installed system

import subprocess
import libcalamares

root_mount_point = libcalamares.globalstorage.value("rootMountPoint")
   
def run():

    RSYNC_CMD = "rsync -vaRI"
    INSTALL_LOG = "/home/liveuser/endeavour-install.log"

    subprocess.call(RSYNC_CMD.split(' ') + [INSTALL_LOG] + [root_mount_point])
