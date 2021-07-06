#!/bin/bash

BASEDIR=`cd "$(dirname $0)/.." >/dev/null; pwd`
PROJECTDIR=`cd "$BASEDIR/../.." >/dev/null; pwd`
echo "work on $BASEDIR"
cd $BASEDIR

# 备份sun8i-h3-atom_n.dtb,将 sun8i-h3-atom_n.dtb 替换到 /boot/sun8i-h3-atom_n.dtb
sudo mv /boot/sun8i-h3-atom_n.dtb /boot/sun8i-h3-atom_n.dtb.backup
sudo cp $PROJECTDIR/sun8i-h3-atom_n.dtb /boot/

# Cloc软连接到WorkSpace
ln -s $BASEDIR ~/WorkSpace/

# 脚本添加运行权限并软连到WorkSpace
chmod +x $PROJECTDIR/WorkSpace/Scripts/start_ui_clock.sh
mkdir -p ~/WorkSpace/Scripts/services
ln -s $PROJECTDIR/WorkSpace/Scripts/services/ui-clock.service ~/WorkSpace/Scripts/services/
ln -s $PROJECTDIR/WorkSpace/Scripts/start_ui_clock.sh ~/WorkSpace/Scripts/

# 下载2个字体文件：“STHeiti Light.ttc”，“PingFang.ttc”，拷贝到$BASEDIR/fonts
cd $BASEDIR/fonts
if [ ! -f "$BASEDIR/fonts/STHeiti%20Light.ttc" ]; then
 wget https://gitee.com/coolflyreg163/quark-n/attach_files/603438/download/STHeiti%20Light.ttc
fi
if [ ! -f "$BASEDIR/fonts/PingFang.ttc" ]; then
 wget https://gitee.com/coolflyreg163/quark-n/attach_files/603439/download/PingFang.ttc
fi

# 安装增加服务并开机启动
cd $BASEDIR
# 安装依赖
sudo python -m pip install -r requirements.txt
sudo ln -s $PROJECTDIR/WorkSpace/Scripts/services/ui-clock.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ui-clock

read -p "Ui-clock installation completed, do you want to restart the system to enable service? [y/n] " isOK
echo "you entered: $isOK"
case $isOK in y)

sudo reboot
done

esac