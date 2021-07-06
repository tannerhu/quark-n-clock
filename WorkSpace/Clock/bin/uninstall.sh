#!/bin/bash

BASEDIR=`cd "$(dirname $0)/.." >/dev/null; pwd`
PROJECTDIR=`cd "$BASEDIR/../.." >/dev/null; pwd`
echo "work on $BASEDIR"
cd $BASEDIR

# 停止ui-clock服务并从开机启动服务中移除
sudo systemctl stop ui-clock
sudo systemctl disable ui-clock
sudo systemctl daemon-reload
cd /lib/systemd/system/
sudo rm -rf ./ui-clock.service

# 删除服务和脚本的软连接
cd ~/WorkSpace/Scripts/services/
sudo rm -rf ./ui-clock.service
cd ~/WorkSpace/Scripts/
sudo rm -rf ./start_ui_clock.sh

# 删除Clock软连
cd ~/WorkSpace/
sudo rm -rf ./Clock

# 还原sun8i-h3-atom_n.dtb
sudo mv /boot/sun8i-h3-atom_n.dtb.backup /boot/sun8i-h3-atom_n.dtb