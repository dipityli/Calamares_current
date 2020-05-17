#!/bin/python3

# Simple
# Just run the script, no aditional config

import subprocess

def run():
    """
    Installing base system. Please be patient!
    """
    
    SCRIPT_PATH = "/usr/lib/calamares/modules/base_install.sh"

#cleaner_script.sh"
    
    try:
        subprocess.call([SCRIPT_PATH])
    except:
        pass
