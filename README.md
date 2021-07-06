<p align="center"><img width="400" src="https://image.haxbk.com/blog/quark-n.jpg"></p>
<h2 align="center">quark-n-clock</h2>

# quark-n
quark-n 即（quark-core+Atom-Shield-N）的一些使用说明：[quark-n基础使用说明](https://haxbk.com/pages/144bc7/?loadPage=1)


本项目基于：[coolflyreg163/quark-n](https://gitee.com/coolflyreg163/quark-n) 进行部分修改

### 使用ui-clock（新的dts的中的蓝色led设备）
1. 安装ui-clock
   ```bash
   mkdir ~/Git && cd ~/Git
   git clone -b https://github.com/tannerhu/quark-n-clock.git
   sh quark-n-clock/WorkSpace/Clock/bin/install.sh
   ```
   注意两个字体文件比较大  
   可以在 git clone之后自己行下载将资源放至项目quark-n-clock/WorkSpace/Clock/fonts/目录下以加快安装速度  
   https://gitee.com/coolflyreg163/quark-n/attach_files/603438/download/STHeiti%20Light.ttc
   https://gitee.com/coolflyreg163/quark-n/attach_files/603439/download/PingFang.ttc
   
2.  卸载ui-clock
   ```bash
   sh ~/Git/quark-n-clock/WorkSpace/Clock/bin/uninstall.sh
   # 要删源码的话执行
   rm -rf ~/Git/quark-n
   ```

3. 服务启停命令：
   1. 启动 （手动启动后按Ctrl + C可脱离）
        ```bash
        sudo systemctl start ui-clock
        ```
   2. 停止
        ```bash
        sudo systemctl stop ui-clock
        ```
   3. 查看状态
        ```bash
        sudo systemctl status ui-clock
        ```

#### 操作方式
1. GPIO按钮操作
   1. 按一下松开，界面上元素循环显示，不同界面，有不同反应
   2. 长按会显示进度条，根据时间不同，有不同的功能
      1. 长按 小于 2秒，不做任何操作
      2. 长按 大于等于 2秒 和 小于 3秒之间，界面显示YES，执行确认操作
      3. 长按 大于等于 3秒 和 小于 5秒之间，界面显示Menu View，进入到菜单界面
      4. 长按 大于等于 5秒 和 小于 10秒之间，界面目前无任何操作，会渐渐显示出POWER OFF
      5. 长按 大于等于 10秒，关机
2. 鼠标操作
   1. 点击界面元素，会有变化，不同界面有不同反应
3. 界面说明
   1. 除了菜单界面的，任意界面，将鼠标移动到最左侧，将显示进入菜单的提示，点击鼠标即可进入菜单界面
   2. 欢迎界面
      1. 无任何操作，定时跳转到数字表盘
   3. 数字表盘界面
      1. 界面元素，分为4行
         1. 第一行循环显示，鼠标可点击
            1. CPU温度 + CPU占比
            2. MEM（内存）剩余空间 + 使用量占比
            3. DSK（磁盘，TF或EMMC）剩余空间 + 使用量占比
         2. 第二行时间，12/24小时切换显示，鼠标可点击
         3. 第三行日期
         4. 第四行，鼠标可点击
            1. IP + 下载速度
            2. 上行速度 + 下载速度
      2. GPIO单按，同时循环以上所有元素
   4. 菜单界面，任意界面长按 大于等于 3秒 和 小于 5秒之间，界面显示Menu View，进入到菜单界面
      1. 界面元素
         1. 时钟：切换到数字表盘（由群内大神 “海 风” 提供原始Clock界面程序）
         2. 孙悟空：开启关闭wukong-robot。需要修改后的悟空版本。参见 https://gitee.com/coolflyreg163/wukong-in-quark-n
         3. 相机：可以支持PS3 Eye摄像头进行拍照，或者其他USB免驱动摄像头
         4. 相册：可以查看通过摄像头拍摄的照片
         5. 启动画面：切换启动图
         6. 设置：正在开发中
         7. 关闭：退出ui_clock
      2. GPIO操作
         1. 长按 大于等于 2秒 和 小于 3秒之间，界面显示YES时，执行确认操作
      3. 其他功能正在开发中

#### 功能列表
- [X] 数字表盘
- [X] 启动画面：切换启动欢迎图界面
- [X] 相机：从USB摄像头拍照
- [X] 相册：查看摄像头拍照的列表
- [X] 孙悟空：集成wukong-robot，需细化功能需求
- [ ] 加入MPU6050，进行姿态操作，增加甩飞Quark-N的几率
- [ ] 实现设置界面的功能，可调整一些参数


#### Linux下声卡独占的原因和解决
简单解决办法如下： 在/boot/defaults/loader.conf或/etc/sysctl.conf中加入下面两行。

hw.snd.pcm0.vchans=4
hw.snd.maxautovchans=4

#### 与WuKong-robot共同使用
**注意：需要先执行：Linux下声卡独占的原因和解决**
1. 备份原始自带的WuKong
   ```bash
   cd /home/pi/WorkSpace/WuKong
   mv wukong-robot wukong-robot_bak
   ```
2. 从 https://gitee.com/coolflyreg163/wukong-in-quark-n 下载WuKong
   ```bash
   cd /home/pi/WorkSpace/WuKong
   git clone https://gitee.com/coolflyreg163/wukong-in-quark-n wukong-robot
   ```
3. 创建所需目录，执行如下命令：
   ```bash
   mkdir /home/pi/WorkSpace/WuKong/wukong-robot/temp
   chmod 777 /home/pi/WorkSpace/WuKong/wukong-robot/temp
   ```
4. 把这个库里的 /WuKong/contrib/LcdDisplay.py 替换到 /home/pi/.wukong/contrib/ 文件夹下的同名文件
   ```bash
   cp ~/Git/quark-n/WuKong/contrib/LcdDisplay.py /home/pi/.wukong/contrib/
   ```
5. 在 /home/pi/.wukong/config.yml 中添加配置。注意要符合格式
   ```yaml
   quark_ui:
       api_host: 'http://127.0.0.1:4096'
       validate: '57b7d993ffbd75aca3fe2060cf204f93' 
       enable: true
   ```
5. 目前snowboy的在线训练无法使用了，暂时在配置中改为：hotword: 'wukong.pmdl'，唤醒词：孙悟空
6. 其他可以参考wukong-robot原版的配置
7. 如果需要使用悟空进行拍照，需要安装fswebcam，运行如下命令安装
   ```bash
   sudo apt-get install fswebcam
   ```
