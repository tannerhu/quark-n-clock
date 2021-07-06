#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from datetime import datetime
import logging
import logging.config
import pygame
from ui.core import UIManager, BaseUI
from ui.theme import *
from utils.stepper import Stepper
from utils.sysinfo import *
from utils.textcolor import *
from utils import runAsync

logger = logging.getLogger('ui.clock')

class ClockUI(BaseUI):

    showTick = 0
    NET_STATS = []
    INTERFACE = 'wlan0'
    # 步进步设置Stepper(最小值, 最大值,步进单位,当前值) 设置点击后可变化显示状态的数量
    sysInfoShowType = Stepper(0, 2, 1, 0)
    timeShowType = Stepper(0, 1, 1, 0)
    dateShowType = Stepper(0, 0, 1, 0)
    netShowType = Stepper(0, 1, 1, 0)

    windowSize = UIManager().getWindowSize()
    window_width = windowSize[0]
    window_height = windowSize[1]
    # 对象矩形框设置
    if window_width == 320:
        # pygame.Rect(left, top, width, height)
        sysInfoRect = pygame.Rect(0, 0, UIManager().getWindowSize()[0], int(window_height * (30 / 135)))
        timeRect = pygame.Rect(0, int(window_height * (31 / 135)), UIManager().getWindowSize()[0], int(window_height * (58 / 135)))
        dateRect = pygame.Rect(0, int(window_height * (88 / 135)), UIManager().getWindowSize()[0], int(window_height * (24 / 135)))
        netRect = pygame.Rect(0, int(window_height * (113 / 135)), UIManager().getWindowSize()[0], int(window_height * (22 / 135)))
    else:
        sysInfoRect = pygame.Rect(0, 0, UIManager().getWindowSize()[0], 30)
        timeRect = pygame.Rect(0, 31, UIManager().getWindowSize()[0], 58)
        dateRect = pygame.Rect(0, 88, UIManager().getWindowSize()[0], 24)
        netRect = pygame.Rect(0, 113, UIManager().getWindowSize()[0], 22)

    prevSecondIntValue = 0
    RX_RATE = 0
    TX_RATE = 0

    lastCpuInfo = readCpuInfo()
    cpuUsef = 0
    memInfo = get_mem_info()
    dskInfo = get_disk_info()
    hostIp = get_host_ip()

    cputemp = 0

    months = ['January', 'February', 'March', 'April', 'May', 
    'June', 'July', 'August', 'September', 'October', 'November', 'December']
    # days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun' ]
    days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日' ]

    def rx(self):
        ifstat = open('/proc/net/dev').readlines()
        for interface in  ifstat:
            if self.INTERFACE in interface:
                stat = float(interface.split()[1])
                self.NET_STATS[0:] = [stat]

    def tx(self):
        ifstat = open('/proc/net/dev').readlines()
        for interface in  ifstat:
            if self.INTERFACE in interface:
                stat = float(interface.split()[9])
                self.NET_STATS[1:] = [stat]

    def on_shown(self):
        self.showTick = pygame.time.get_ticks()
        self.cputemp = cputemp()
        self.rx()
        self.tx()
        self.lastCpuInfo = readCpuInfo()
        pass

    def on_hidden(self):
        pass

    def onKeyRelease(self, isLongPress, pushCount, longPressSeconds, keyIndex):
        if not isLongPress and pushCount == 1:
            self.sysInfoShowType.next()
            self.timeShowType.next()
            self.dateShowType.next()
            self.netShowType.next()

    def onMouseDown(self, event):
        if self.sysInfoRect.collidepoint(pygame.mouse.get_pos()):
            self.sysInfoShowType.next()
        elif self.timeRect.collidepoint(pygame.mouse.get_pos()):
            self.timeShowType.next()
        elif self.dateRect.collidepoint(pygame.mouse.get_pos()):
            self.dateShowType.next()
        elif self.netRect.collidepoint(pygame.mouse.get_pos()):
            self.netShowType.next()
    
    def onTouchEnd(self, event):
        if self.sysInfoRect.collidepoint(event):
            self.sysInfoShowType.next()
        elif self.timeRect.collidepoint(event):
            self.timeShowType.next()
        elif self.dateRect.collidepoint(event):
            self.dateShowType.next()
        elif self.netRect.collidepoint(event):
            self.netShowType.next()
        pass

    def update(self, surface = None):
        surface = UIManager().getSurface()
        windowSize = UIManager().getWindowSize()
        window_width = windowSize[0]
        window_height = windowSize[1]
        surface.fill(color_black)

        now = datetime.now()
        today = datetime.today()

        minute = now.strftime('%M')
        second = now.strftime('%S')
        hour = int(now.strftime('%H'))
        month = now.strftime('%m')
        date = now.strftime('%d')
        year = now.strftime("%Y")
        day = today.weekday()
        day = self.days[day]
        secondIntValue = int(second)
        # RX_RATE = 0.0
        # TX_RATE = 0.0
        if self.prevSecondIntValue != secondIntValue:
            # mouseLastMotion = mouseLastMotion - 1
            rxstat_o = list(self.NET_STATS)
            self.rx()
            self.tx()
            if len(self.NET_STATS) > 0:
                RX = float(self.NET_STATS[0])
                RX_O = rxstat_o[0]
                TX = float(self.NET_STATS[1])
                TX_O = rxstat_o[1]
                self.RX_RATE = round((RX - RX_O)/1024/1024,3)
                self.TX_RATE = round((TX - TX_O)/1024/1024,3)
            else:
                RX = 0.0
                RX_O = 0
                TX = 0.0
                TX_O = 0
                self.RX_RATE = 0
                self.TX_RATE = 0

            self.memInfo = get_mem_info()
            self.dskInfo = get_disk_info()
            self.hostIp = get_host_ip()

            cpuInfo = readCpuInfo()
            self.cpuUsef = round(calcCpuUsage(self.lastCpuInfo, cpuInfo), 1) # getCPUuse()
            self.lastCpuInfo = cpuInfo

        cpuUsef = self.cpuUsef
        memInfo = self.memInfo
        memStr = "MEM {0}M".format(memInfo['free'])
        memUse = memInfo['percent']
        dskInfo = self.dskInfo
        dskStr = "DSK {0}".format(dskInfo['free'])
        dskUse = dskInfo['percent']

        if secondIntValue % 5 == 0:
            self.cputemp = cputemp()

        am = 'AM'
        
        if self.timeShowType.current() == 0 and hour > 12:
            hour = hour-12
            am = 'PM'

        shour = str(hour)
        if len(shour) == 1:
            shour = '0' + shour
        timeStr = shour + ':' + minute
        # largeFont.render(内容, 是否抗锯齿, 颜色)
        # timeText = largeFont.render(timeStr, True, color_green)
        secondText = self.get_cache('secondText_{}'.format(second), lambda: middleFont.render(second, True, color_green))
        amText = self.get_cache('amText_{}'.format(am), lambda: middleFont.render(am, True, color_green))

        if self.sysInfoShowType.current() == 0:
            cputempf = "CPU {0} C".format(self.cputemp)
            sysText = self.get_cache('sysText_{}'.format(cputempf), lambda: miFont.render(cputempf, True, tempColor(int(self.cputemp))))
            sysUseText = self.get_cache('sysUseText_{}'.format(cputempf), lambda: miFont.render(str(cpuUsef) + '%', True, cpuUseColor(int(cpuUsef))))
        if self.sysInfoShowType.current() == 1:
            sysText = self.get_cache('sysText_{}'.format(memStr), lambda: miFont.render(memStr, True, memUseColor(memUse)))
            sysUseText = self.get_cache('sysUseText_{}'.format(str(memUse)), lambda: miFont.render(str(memUse) + '%', True,  memUseColor(memUse)))
        if self.sysInfoShowType.current() == 2:
            sysText = self.get_cache('sysText_{}'.format(dskStr), lambda: miFont.render(dskStr, True, dskUseColor(float(dskUse))))
            sysUseText = self.get_cache('sysUseText_{}'.format(str(dskUse)), lambda: miFont.render(str(dskUse), True, dskUseColor(float(dskUse))))
        rxStr = '' + str(self.RX_RATE) + ' M/s'
        txStr = '' + str(self.TX_RATE) + ' M/s'
        netSpeedInText = self.get_cache('rxStr_{}'.format(rxStr), lambda: tinyFont.render(rxStr, True, netStatsColor(self.RX_RATE)))
        netSpeedOutText = self.get_cache('txStr_{}'.format(txStr), lambda: tinyFont.render(txStr, True, netStatsColor(self.TX_RATE)))

        ip = self.hostIp
        ipText = self.get_cache('ip_{}'.format(ip), lambda: miniFont.render(ip, True, color_white))

        if window_width == 320:
            timeText = self.get_cache('timeText_{}'.format(timeStr), lambda: getAppFont(120, 'DIGIT').render(timeStr, True, color_green)) # largeFont
            # yearText = self.get_cache('yearText_{}'.format(year), lambda: getAppFont(50, 'DIGIT').render(year, True, color_green))
            dayText = self.get_cache('dayText_{}'.format(day), lambda: getAppFont(36, 'PingFang').render(day, True, color_green))
            monthText = self.get_cache('monthText_{}'.format(year + '-' + month + '-' + date), lambda: getAppFont(46, 'DIGIT').render(year + '-' + month + '-' + date, True, color_green))
            surface.blit(sysText, (10,0))
            surface.blit(sysUseText, (window_width - sysUseText.get_width() - 2,0))
            surface.blit(timeText, (6, int(window_height * (16 / 135))))
            surface.blit(secondText, (window_width - secondText.get_width(), int(window_height * (52 / 135))))
            surface.blit(monthText, (15, int(window_height * (86 / 135))))
            # surface.blit(yearText, (145,120))
            if self.timeShowType.current() == 0:
                surface.blit(amText,(window_width - amText.get_width(), int(window_height * (22 / 135))))
            surface.blit(dayText,(window_width - dayText.get_width(), int(window_height * (86 / 135))))

            if self.netShowType.current() == 1:
                surface.blit(netSpeedInText, (window_width - netSpeedInText.get_width(), window_height - 23))
                surface.blit(netSpeedOutText, (window_width / 2 - netSpeedOutText.get_width(), window_height - 23))
            else:
                surface.blit(ipText,(10, window_height - 23))
                surface.blit(netSpeedInText, (window_width - netSpeedInText.get_width(), window_height - 23))
        else:
            timeText = self.get_cache('timeText_{}'.format(timeStr), lambda: getAppFont(82, 'DIGIT').render(timeStr, True, color_green)) # largeFont
            # yearText = self.get_cache('yearText_{}'.format(year), lambda: smallFont.render(year, True, color_green))
            dayText = self.get_cache('dayText_{}'.format(day), lambda: getAppFont(24, 'PingFang').render(day, True, color_green))
            monthText = self.get_cache('monthText_{}'.format(year + '-' + month + '-' + date), lambda: smallFont.render(year + '-' + month + '-' + date, True, color_green))
            surface.blit(sysText, (10,0))
            surface.blit(sysUseText, (window_width - sysUseText.get_width() - 2,0))
            surface.blit(timeText, (4,16))
            surface.blit(secondText, (190, 52))
            surface.blit(monthText, (15,86))
            # surface.blit(yearText, (145,120))
            if self.timeShowType.current() == 0:
                surface.blit(amText,(190,22))
            surface.blit(dayText,(window_width - dayText.get_width(),86))

            if self.netShowType.current() == 1:
                surface.blit(netSpeedInText, (window_width - netSpeedInText.get_width(), window_height - 23))
                surface.blit(netSpeedOutText, (window_width / 2 - netSpeedOutText.get_width(), window_height - 23))
            else:
                surface.blit(ipText,(10, window_height - 23))
                surface.blit(netSpeedInText, (window_width - netSpeedInText.get_width(), window_height - 23))
        
        self.prevSecondIntValue = secondIntValue
        # welcomeTxt = bigFont.render(ClockUI.__name__, True, color_white)
        # surface.blit(welcomeTxt, (window_width / 2 - welcomeTxt.get_width() / 2, window_height / 2 - welcomeTxt.get_height() / 2))

        # pygame.draw.rect(surface, (255,255,255), self.sysInfoRect, 1)
        # pygame.draw.rect(surface, (255,255,255), self.timeRect, 1)
        # pygame.draw.rect(surface, (255,255,255), self.dateRect, 1)
        # pygame.draw.rect(surface, (255,255,255), self.netRect, 1)
        pass

    pass
