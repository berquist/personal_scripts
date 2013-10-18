#!/bin/sh

date=`date "+%Y-%m-%dT%H_%M_%S"`

HOME=/home/eric
SOURCE=$HOME
BACKUPDIR=/media/Backup/BackupDir

rsync -azPE --exclude-from '/home/eric/opt/bin/scripts/backup_exclude_list_gold.txt' \
    --link-dest=$BACKUPDIR/current $SOURCE $BACKUPDIR/back-$date

rm -f $BACKUPDIR/current
ln -s back-$date $BACKUPDIR/current

