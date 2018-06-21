#!/usr/bin/env bash

export CHROOT="${HOME}/data/chroot"
arch-nspawn "${CHROOT}/root" pacman -Syyu
makechrootpkg -c -r "${CHROOT}"
