#!/bin/sh

date=`date "+%Y-%m-%dT%H_%M_%S"`

HOME=erb74@frank.sam.pitt.edu:/home/dlambrecht/erb74
SOURCE=$HOME
BACKUPDIR=/media/Backup/BackupDir/frank

rsync -azPE \
    --link-dest=$BACKUPDIR/current $SOURCE $BACKUPDIR/back-$date

rm -f $BACKUPDIR/current
ln -s back-$date $BACKUPDIR/current

