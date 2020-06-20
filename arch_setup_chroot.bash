#!/usr/bin/env bash

export CHROOT=/home/eric/data/chroot
mkdir -p $CHROOT
mkarchroot $CHROOT/root base-devel
arch-nspawn $CHROOT/root pacman -Syu

# Then, to build a package in the chroot, run the following from the
# dir containing the PKGBUILD:
# makechrootpkg -c -r $CHROOT
