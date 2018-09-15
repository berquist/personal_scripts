#!/usr/bin/env bash

date=`date "+%Y-%m-%dT%H_%M_%S"`

HOME=/home/eric
SOURCE=$HOME
BACKUPDIR=/media/Backup/BackupDir

rsync -azPE \
    --link-dest=$BACKUPDIR/current $SOURCE $BACKUPDIR/back-$date

rm -f $BACKUPDIR/current
ln -s back-$date $BACKUPDIR/current

