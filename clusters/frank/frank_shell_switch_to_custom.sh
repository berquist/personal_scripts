#!/usr/bin/env bash

rm ${HOME}/.bash_profile
rm ${HOME}/.bashrc
ln -sv ${HOME}/dotfiles/.bash_profile.frank ${HOME}/.bash_profile
ln -sv ${HOME}/dotfiles/.bashrc.frank ${HOME}/.bashrc
