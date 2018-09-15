#!/usr/bin/env bash

echo "pulling $HOME/dotfiles..."
cd $HOME/dotfiles
git pull

echo "pulling $HOME/scripts..."
cd $HOME/scripts
git pull

echo "pulling $HOME/modules..."
cd $HOME/modules
git pull

echo "pulling $HOME/buildscripts..."
cd $HOME/buildscripts
git pull
