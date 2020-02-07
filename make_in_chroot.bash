#!/usr/bin/env bash

export CHROOT="${HOME}/data/chroot"
arch-nspawn "${CHROOT}/root" pacman -Syu
makechrootpkg -c -r "${CHROOT}"
