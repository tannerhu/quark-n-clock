#!/bin/bash


BASEDIR=`cd "$(dirname $0)/.." >/dev/null; pwd`
echo "work on $BASEDIR"
cd $BASEDIR


sudo nohup ./main.py restart >> nohup.log 2>&1 & 




