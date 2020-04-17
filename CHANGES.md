list of changes

# month, day
April

17


Issue: some installs are hanging due arch bad mirrors

Test: changing `pacman_flags = "-S"` to `pacman_flags = "-Sy"`at `def install` function at `src/modules/packages/main.py`

Possible new issue: if the repos keep receiving updates the mirrors may be synched from time to time, which can make install slower. If proven can sync once before installing. Notice the error is appearing even if -Sy is executed at pacstrap module.

##########

src/modules/pacstrap/alternative_pacstrap


Is an alternative module that uses pacstrap to install base and pacman to install other "essencial packages" listed on the very same module. When running pacman installes package by package, increasing the verbose mode and making easier to detect issues on repo/mirrors/signature


The current pacstrap module uses only pacstrap
