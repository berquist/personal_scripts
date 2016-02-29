### VirtualBox installation instructions!

## Installation

# ...do disk partitioning with cfdisk...
# partition type/label: dos -> 83 Linux
cfdisk
mkfs.ext4 /dev/sda1
mount /mnt /dev/sda1
pacstrap -i /mnt base base-devel
genfstab -U /mnt > /mnt/etc/fstab
cat /mnt/etc/fstab
arch-chroot /mnt /bin/bash
nano /etc/locale.gen
locale-gen
echo LANG=en_US.UTF-8 > /etc/locale.conf
ln -sf /usr/share/zoneinfo/US/Eastern /etc/localtime
hwclock --systohc --utc
echo hydrogen > /etc/hostname
systemctl enable dhcpcd.service
mkinitcpio -p linux
passwd
pacman -S grub
grub-install --recheck /dev/sda
grub-mkconfig -o /boot/grub/grub.cfg
exit
umount -R /mnt
# reboot

## Install VBox stuff

pacman -S virtualbox-guest-utils

## Adding a group/user

EDITOR=nano visudo
groupadd sudo

useradd -m -s /usr/bin/zsh eric
passwd eric
usermod -aG sudo eric
