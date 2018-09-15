#!/usr/bin/env bash

export CHROOT=/media/Backup/chroot
# mkdir -p $CHROOT
# mkarchroot $CHROOT/root base-devel
arch-nspawn $CHROOT/root pacman -Syyu

# Then, to build a package in the chroot, run the following from the
# dir containing the PKGBUILD:
# makechrootpkg -c -r $CHROOT
