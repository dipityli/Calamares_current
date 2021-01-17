#!/bin/python3

# Simple
# Just run the script, no aditional config

import subprocess

def run():
    """
    Installing user packages. Please be patient!
    """
    
    SCRIPT_PATH = "/usr/lib/calamares/modules/user_pkglist/pkglist_install.sh"

    
    try:
        subprocess.call([SCRIPT_PATH])
    except:
        pass
