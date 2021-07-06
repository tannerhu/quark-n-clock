#!/bin/bash

BASEDIR=`cd "$(dirname $0)/.." >/dev/null; pwd`
PROJECTDIR=`cd "$BASEDIR/../.." >/dev/null; pwd`
echo "work on $BASEDIR"
cd $BASEDIR

cd $PROJECTDIR
sudo systemctl stop ui-clock && git pull origin master