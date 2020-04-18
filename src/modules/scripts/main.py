#!/bin/python3

# Simple
# Just run the script, no aditional config

import subprocess

def run():
    """
    Cleaning the system and making final adjusts
    """
    
    SCRIPT_PATH = "/usr/bin/cleaner_script.sh"
    
    try:
        subprocess.call([SCRIPT_PATH])
    except:
        pass
