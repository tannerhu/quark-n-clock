#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import time
import logging
from queue import Queue
from core import Singleton, Event, EventDispatcher
from system.config import Config
import os


class UIManager(metaclass=Singleton):
    """
    All UI manager
    """

    current_ui = None
    window_size = None
    surface = None
    __ui_dict = {}
    __ui_stack = []

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def setWindowSize(self, window_size):
        self.window_size = window_size

    def setSurface(self, surface):
        self.surface = surface

    def getSurface(self):
        return self.surface

    def getWindowSize(self):
        return self.window_size

    def init(self):
        from .welcome import WelcomeUI
        from .clock import ClockUI
        from .menu import MenuUI
        self.__ui_dict[WelcomeUI.__name__] = WelcomeUI(0)
        self.__ui_dict[ClockUI.__name__] = ClockUI(1)
        self.__ui_dict[MenuUI.__name__] = MenuUI(2)
        # self.__ui_dict[WelcomeUI.__name__].show()
        self.__ui_dict[MenuUI.__name__].show()
        pass

    def update(self):
        if self.current() is not None:
            self.current().update()

        for ui_name in self.__ui_dict:
            if self.__ui_dict[ui_name] is not self.current():
                self.__ui_dict[ui_name].update_offscreen()

    def current(self):
        if len(self.__ui_stack) == 0:
            return None
        return self.__ui_stack[-1:][0]

    def push(self, ui):
        self.__ui_stack.append(ui)
        pass

    def pop(self):
        return self.__ui_stack.pop()

    def replace(self, ui):
        self.pop()
        self.push(ui)
        pass

    def get(self, ui_name):
        return self.__ui_dict[ui_name]

    pass


class BaseUI:
    """
    This is ui base class
    """

    ui_index = 0

    controls = None

    def __init__(self, ui_index):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.ui_index = ui_index
        self.event_dispatcher = EventDispatcher()
        self.on_create()

    def on_create(self):
        self.logger.debug('UI created: {0}'.format(self))
        pass

    def add_control(self, control):
        if self.controls is None:
            self.controls = []
        self.controls.append(control)

    def paint(self):
        pass

    def update(self):
        pass

    def update_offscreen(self):
        pass

    def onMouseDown(self, event):
        pass
    
    def onMouseUp(self, event):
        pass

    def onMouseMove(self, event):
        pass

    def onKeyPush(self, pushCount):
        pass

    def onKeyRelease(self, isLongPress, pushCount, longPressSeconds):
        pass

    def onKeyLongPress(self, escapedSeconds):
        pass

    # def process_cmds(self, cmds):
    #     if len(cmds) <= 0:
    #         return False

    #     if self.controls is not None:
    #         for c in self.controls:
    #             if c.process_cmds(cmds):
    #                 return True

    #     for serial_cmd in cmds:
    #         if len(serial_cmd) > 3 and serial_cmd[:3] == 'BN:':
    #             try:
    #                 btn_index = int(serial_cmd[3:])
    #                 self.logger.info("Release BN {0}".format(btn_index))
    #             except ValueError as e:
    #                 self.logger.warning('Error cmd: {0}'.format(serial_cmd))

    #         if len(serial_cmd) > 3 and serial_cmd[:3] == 'BS:':
    #             try:
    #                 btn_index = int(serial_cmd[3:])
    #                 self.logger.info("Press BS {0}".format(btn_index))
    #             except ValueError as e:
    #                 self.logger.warning('Error cmd: {0}'.format(serial_cmd))

    #     return False

    def __show(self):
        ui_manager = UIManager()
        self.on_shown()

    def show(self):
        ui_manager = UIManager()
        ui_manager.push(self)
        self.__show()

    def replace_current(self):
        ui_manager = UIManager()
        ui_manager.replace(self)
        self.__show()

    def hide(self):
        ui_manager = UIManager()
        ui_manager.pop()
        self.on_hidden()
        ui_manager.current().__show()

    def on_shown(self):
        if self.controls is not None:
            self.logger.debug('UI on_shown: {0}, controls: {1}'.format(self, self.controls))
            for c in self.controls:
                c.paint()
        pass

    def on_hidden(self):
        pass

    pass


class BaseControl(BaseUI):

    owner = None
    x = 0
    y = 0
    btn = None

    def __init__(self, owner):
        super().__init__(0)
        self.owner = owner

    def init(self, x, y, btn, **kwargs):
        self.x = x
        self.y = y
        self.btn = btn

    def do_command(self):
        pass

    def process_cmds(self, cmds):
        if len(cmds) == 0 or self.btn is None:
            return False

        cmd = cmds[0]

        if cmd == 'BN:{0}'.format(self.btn):
            self.do_command()
        pass

    def on_changed(self, value):
        pass


class ControlEvent(Event):
    CHANGED = "CHANGED"