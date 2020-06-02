list of changes

# month, day

May

26

pacstrap as bash script is implemented at branch "may_2020" and has a compiled version for tests as calamares_test


16

Merging april branch and pushing calamares to 3.2.24


April

22

shellprocess.conf timeout changed to 108000

18

Moved shellprocess module to the last position at settings.conf{_online,_offline} In order to prevent install failure due an error in the script or it's timeout value

ALso implemented scripts module, which is a simple python that calls desired bash scripts as a replacement for shellprocess

17


Issue: some installs are hanging due arch bad mirrors

Test: changing `pacman_flags = "-S"` to `pacman_flags = "-Sy"`at `def install` function at `src/modules/packages/main.py`

Possible new issue: if the repos keep receiving updates the mirrors may be synched from time to time, which can make install slower. If proven can sync once before installing. Notice the error is appearing even if -Sy is executed at pacstrap module.

##########

src/modules/pacstrap/alternative_pacstrap


Is an alternative module that uses pacstrap to install base and pacman to install other "essencial packages" listed on the very same module. pacman installs package by package, increasing verbose mode and making easier to detect issues on repo/mirrors/signature


The current pacstrap module uses only pacstrap

##########

Following options were changed at settings.conf for all files

prompt-install

disable-cancel-during-exec

quit-at-end
