
#!/bin/python3


import subprocess

# Downloads .yaml file with list of packages to be displayed at netinstall screen. Alternative to using upstream file since calamares is having trouble to access github.

# Need a solution to filter between normal ISO and Nvidia :(

# Need to set calamares to check local list of packages and set new module at welcome screen at some point after internet detection. The file is downloaded and used at live environment only.

# Variations
# https://github.com/endeavouros-team/install-scripts/raw/master/netinstall.yaml
# https://raw.githubusercontent.com/endeavouros-team/install-scripts/master/netinstall.yaml

# https://github.com/endeavouros-team/install-scripts/raw/master/netinstall_nvidia.yaml
# https://raw.githubusercontent.com/endeavouros-team/install-scripts/master/netinstall_nvidia.yaml

def run():

    GET_YAML = "wget https://github.com/endeavouros-team/install-scripts/raw/master/netinstall.yaml"
    MV_YAML= "mv -f netinstall.yaml /usr/share/calamares/netinstall.yaml"
     
    try:
        subprocess.call(GET_YAML.split(' ')) 
        subprocess.call(MV_YAML.split(' '))
    except:
        pass
