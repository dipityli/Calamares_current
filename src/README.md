Basic EndeavourOS/Portergos config files

Branding folder:
Contains a minimum set of files to make a customized slide presentation in the install process

Modules folder:


```
copy_kernel module

Used in offline install. Created because old python code of initramfs was changed to c++ and injected to a library. 
It copies linux and linux-lts kernel if it exist from live environment to target system. Process is necessary because archiso .sfs doesn't contain the kernel which is present on another path.
```

```
pacstrap module

Used in online install. Created to allow pacstrap command to install a base and any other packages. The module also uses automirror script if installed, otherwise it uses reflector to select best mirrors, so install is faster.
Module also uses haveged package to provide entropy for keyring generation.
```

```
update_system

Used in offline install. Is no longer used since some of the steps are executed after install at welcome screen. It allows an offline install to select best mirrors and update system after offline install.
```

```
initcpio/InitcpioJob.cpp

Modified version from calamares. Instead of using mkinitcpio -p "kernel" (which comes from initramfs module) uses mkinitcpio -P; this way iso can have multiple kernels installed and the install process is able to generate initramfs to all of them.
```
