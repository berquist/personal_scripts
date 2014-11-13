#!/bin/sh

echo "pulling $HOME/dotfiles..."
cd $HOME/dotfiles
git pull

echo "pulling $HOME/scripts..."
cd $HOME/scripts
git pull

echo "pulling $HOME/modules..."
cd $HOME/modules
git pull

echo ""
cd $HOME/buildscripts
git pull
