#!/bin/python3

# Simple
# Just run the script, no aditional config

import subprocess
import libcalamares

root_mount_point = libcalamares.globalstorage.value("rootMountPoint")

def run():
    """
    Installing base system. Please be patient!
    """
    
# To use as bash script need to get root path file before get_root_username
    try:
     subprocess.call(['rm', '/tmp/chrootpath.txt'])
     with open('/tmp/chrootpath.txt', 'w') as file:
      root_mount_point = libcalamares.globalstorage.value("rootMountPoint")
      file.write(root_mount_point)
      file.close()
    except:
     pass # doing nothing on exception

    SCRIPT_PATH = "/usr/lib/calamares/modules/pacstrap/base_install.sh"

#cleaner_script.sh"
    
    try:
        subprocess.call([SCRIPT_PATH])
    except:
        pass