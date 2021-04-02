#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import sys
import logging
import logging.config
from ui.core import UIManager, BaseUI
from ui.theme import *
from utils.GIFImage import GIFImage
from system.config import Config

logger = logging.getLogger('ui.video')

class VideoUI(BaseUI):

    showTick = 0
    current_img = None
    current_filename = ''
    fileObjs = []
    target_index = 0

    def on_shown(self):
        target_index = 0
        pic_path = Config().get('camera.video_path', '/home/pi/Videos/')
        if os.path.exists(pic_path) and os.path.isdir(pic_path):
            self.fileObjs = os.listdir(pic_path)
        if len(self.fileObjs) > 0 and target_index < len(self.fileObjs):
            filepath = os.path.join(pic_path, self.fileObjs[target_index])
            self.loadFile(filepath)

        self.target_index = target_index
        self.showTick = pygame.time.get_ticks()
        pass

    def loadFile(self, path):
        if os.path.exists(path) is False:
            self.current_img = None
            return
        if os.path.isfile(path):
            logger.info("path = {}".format(path))
            if path.lower().endswith('.mp4'):
                self.current_img = pygame.image.load(os.path.join(sys.path[0], 'images/icon_set2', 'mp4.png'))
            elif path.lower().endswith('.avi') or path.lower().endswith('.mpg') or path.lower().endswith('.mpeg'):
                # self.current_img = pygame.transform.scale(pygame.image.load(path), UIManager().getWindowSize())
                self.current_img = pygame.image.load(os.path.join(sys.path[0], 'images/icon_set2', 'shipin.png'))
            # elif path.lower().endswith('.gif'):
            #     self.current_img = GIFImage(path)
            else:
                self.current_img = pygame.image.load(os.path.join(sys.path[0], 'images/icon_set3', 'doc.png'))
        else:
            self.current_img = pygame.image.load(os.path.join(sys.path[0], 'images/icon_set3', 'folder.png'))
            pass
        self.current_filename = os.path.basename(path)

    def onMouseUp(self, event):
        windowSize = UIManager().getWindowSize()
        window_width = windowSize[0]
        window_height = windowSize[1]
        leftRect = pygame.Rect(3, 5, window_width / 2 - 3, window_height - 10)
        rightRect = pygame.Rect(window_width / 2, 5, window_width / 2, window_height - 10)

        if leftRect.collidepoint(event.pos):
            if (self.target_index - 1) < 0:
                self.target_index = len(self.fileObjs) - 1
            else:
                self.target_index = self.target_index - 1
        if rightRect.collidepoint(event.pos):
            if (self.target_index + 1) >= len(self.fileObjs):
                self.target_index = 0
            else:
                self.target_index = self.target_index + 1
        pic_path = Config().get('camera.video_path', '/home/pi/Videos/')
        filepath = os.path.join(pic_path, self.fileObjs[self.target_index])
        self.loadFile(filepath)
        pass


    def onKeyRelease(self, isLongPress, pushCount, longPressSeconds, keyIndex):
        if not isLongPress and pushCount == 1:
            if keyIndex == 1:
                if (self.target_index - 1) < 0:
                    self.target_index = len(self.fileObjs) - 1
                else:
                    self.target_index = self.target_index - 1
            else:
                if (self.target_index + 1) >= len(self.fileObjs):
                    self.target_index = 0
                else:
                    self.target_index = self.target_index + 1

            
            if len(self.fileObjs) > 0 and self.target_index < len(self.fileObjs):
                pic_path = Config().get('camera.video_path', '/home/pi/Videos/')
                filepath = os.path.join(pic_path, self.fileObjs[self.target_index])
                self.loadFile(filepath)

            return True
        # if isLongPress:
        #     if longPressSeconds == 2:
        #         return True
        #     pass
        return False

    def on_hidden(self):
        pass

    def update(self, surface = None):
        surface = UIManager().getSurface()
        windowSize = UIManager().getWindowSize()
        window_width = windowSize[0]
        window_height = windowSize[1]
        surface.fill(color_black)

        if len(self.fileObjs) == 0:
            welcomeTxt = bigFont.render('No', True, color_white)
            welcome2Txt = bigFont.render('Images', True, color_white)
            surface.blit(welcomeTxt, (window_width / 2 - welcomeTxt.get_width() / 2, 10))
            surface.blit(welcome2Txt, (window_width / 2 - welcome2Txt.get_width() / 2, 60))
        else:
            if self.current_img is not None:
                if self.current_img.__class__.__name__ == pygame.Surface.__name__:
                    surface.blit(self.current_img, (window_width / 2 - self.current_img.get_width() / 2, window_height / 2 - self.current_img.get_height() / 2))
                else:
                    self.current_img.render(surface, (window_width / 2 - self.current_img.get_width() / 2, window_height / 2 - self.current_img.get_height() / 2))
            if self.current_filename is not None:
                nameTxt = zhMiniFont.render(self.current_filename, True, color_white)
                surface.blit(nameTxt, (window_width / 2 - nameTxt.get_width() / 2, 10))

        page = '{}/{}'.format(self.target_index + 1, len(self.fileObjs))
        pageText = miniFont.render(page, True, color_green)
        surface.blit(pageText, (window_width / 2 - pageText.get_width() / 2, window_height - pageText.get_height()))
        pass

    pass