__author__ = 'Allen W'

import pygame as pg
from .. import tool
from .. import constants as c
#所有的植物卡片的名称和属性都保存在单独的list中，每个list index都对应一种植物。
# 比如list index 0 就是太阳花：
# card_name_list[0] 是太阳花卡片的名字，用来获取太阳花卡片的图片。
# plant_name_list[0] 是太阳花的名字，用来获取太阳花卡片的图片。
# plant_sun_list[0] 是种植太阳花需要花费的太阳点数。
# plant_frozen_time_list[0] 是太阳花的冷却时间。
card_name_list = [c.CARD_SUNFLOWER, c.CARD_PEASHOOTER, c.CARD_SNOWPEASHOOTER, c.CARD_WALLNUT, c.CARD_CHERRYBOMB]
plant_name_list = [c.SUNFLOWER, c.PEASHOOTER, c.SNOWPEASHOOTER, c.WALLNUT, c.CHERRYBOMB]
plant_sun_list = [50, 100, 175, 50, 150]
card_list = [0, 1, 2, 3, 4]




#每个植物卡片是一个单独的Card类，用来显示这个植物。
# checkMouseClick函数：判断鼠标是否点击到这个卡片
# canClick：判断这个卡片是否能种植（有没有足够的点数，是否还在冷却时间内）
# update 函数：通过设置图片的透明度来表示这个卡片是否能选择
class Card():
    def __init__(self, x, y, name_index):
        self.loadFrame(card_name_list[name_index])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.name_index = name_index
        self.sun_cost = plant_sun_list[name_index]

    def loadFrame(self, name):
        frame = tool.GFX[name]
        rect = frame.get_rect()
        width, height = rect.w, rect.h

        self.image = tool.get_image(frame, 0, 0, width, height, c.BLACK, 0.8)
    
    def checkMouseClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.rect.x and x <= self.rect.right and
           y >= self.rect.y and y <= self.rect.bottom):
            return True
        return False

    def draw(self, surface):
        surface.blit(self.image, self.rect)



#MenuBar类显示游戏画面上方的植物卡片栏，
# self.sun_value：当前采集的太阳点数
# self.card_list: 植物卡片的list
# setupCards函数：遍历初始化__init__函数中传入这个关卡选好的植物卡片list，依次创建Card类，设置每个卡片的显示位置。
# checkCardClick函数：检查鼠标是否点击了卡片栏上的某个植物卡片，如果选择了一个可种植的卡片，返回结果。
class MenuBar():
    def __init__(self, card_list, sun_value):
        self.loadFrame(c.MENUBAR_BACKGROUND)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 0
        
        self.sun_value = sun_value
        self.card_offset_x = 38
        self.setupCards(card_list)
        self.font = pg.font.SysFont(None, 20)

    def loadFrame(self, name):
        frame_rect = [11, 0, 560, 108]
        frame = tool.GFX[name]
        rect = frame.get_rect()
        width, height = rect.w, rect.h

        self.image = tool.get_image(tool.GFX[name], *frame_rect, c.BLACK, 0.8)

    def createImage(self, x, y, num):
        if num == 1:
            return
        img = self.image
        rect = self.image.get_rect()
        width = rect.w
        height = rect.h
        self.image = pg.Surface((width * num, height)).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        for i in range(num):
            x = i * width
            self.image.blit(img, (x,0))
        self.image.set_colorkey(c.BLACK)
    
    def setupCards(self, card_list):
        self.card_list = []
        x = self.card_offset_x
        y = 7
        for index in card_list:
            x += 55
            self.card_list.append(Card(x, y, index))

    def checkCardClick(self, mouse_pos):
        result = None
        for card in self.card_list:
            if card.checkMouseClick(mouse_pos):
                if card.sun_cost <= self.sun_value:
                    result = (plant_name_list[card.name_index], card.sun_cost)
                break
        return result
    
    def checkMenuBarClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.rect.x and x <= self.rect.right and
           y >= self.rect.y and y <= self.rect.bottom):
            return True
        return False

    def decreaseSunValue(self, value):
        self.sun_value -= value

    def increaseSunValue(self, value):
        self.sun_value += value
    
    def drawSunValue(self):
        width = 30
        msg_image = self.font.render(str(self.sun_value), True, c.NAVYBLUE, c.LIGHTYELLOW)
        msg_rect = msg_image.get_rect()
        msg_w = msg_rect.width
        
        image = pg.Surface([width, 17])
        x = width - msg_w
        
        image.fill(c.LIGHTYELLOW)
        image.blit(msg_image, (x, 0), (0, 0, msg_rect.w, msg_rect.h))
        image.set_colorkey(c.BLACK)

        self.value_image = image
        self.value_rect = self.value_image.get_rect()
        self.value_rect.x = 18
        self.value_rect.y = self.rect.bottom - 20
        
        self.image.blit(self.value_image, self.value_rect)

    def draw(self, surface):
        self.drawSunValue()
        surface.blit(self.image, self.rect)
        for card in self.card_list:
            card.draw(surface)