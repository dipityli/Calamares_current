list of changes

# month, day
April

17

Issue: some install are hanging due arch bad mirrors

Test: changing `pacman_flags = "-S"` to `pacman_flags = "-Sy"`at def install function at src/modules/packages/main.py
