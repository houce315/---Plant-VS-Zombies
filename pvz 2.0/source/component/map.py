__author__ = 'Allen W'

import random
import pygame as pg
from .. import tool
from .. import constants as c

#self.map：二维list，用来保存每个方格的状态。每个entry初始化为 0, 表示可以种植物，值为1时表示这个方格已经种了植物。
# getMapIndex 函数：传入参数是游戏中的坐标位置（比如当前鼠标的位置），返回该位置在地图的哪个方格中。
# getMapGridPos 函数：传入一个方格的index，返回在该方格中种植物的坐标位置。
# showPlant 函数：根据传入的坐标位置，判断该位置所在的方格是否能种植物，如果能种，就返回返回在该方格中种植物的坐标位置。

class Map():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[0 for x in range(self.width)] for y in range(self.height)]

    def isValid(self, map_x, map_y):
        if (map_x < 0 or map_x >= self.width or
            map_y < 0 or map_y >= self.height):
            return False
        return True
    
    def isMovable(self, map_x, map_y):
        return (self.map[map_y][map_x] == c.MAP_EMPTY)
    
    def getMapIndex(self, x, y):
        x -= c.MAP_OFFSET_X
        y -= c.MAP_OFFSET_Y
        return (x // c.GRID_X_SIZE, y // c.GRID_Y_SIZE)
    
    def getMapGridPos(self, map_x, map_y):
        return (map_x * c.GRID_X_SIZE + c.GRID_X_SIZE//2 + c.MAP_OFFSET_X, 
                map_y * c.GRID_Y_SIZE + c.GRID_Y_SIZE//5 * 3 + c.MAP_OFFSET_Y)
    
    def setMapGridType(self, map_x, map_y, type):
        self.map[map_y][map_x] = type

    def getRandomMapIndex(self):
        map_x = random.randint(0, self.width-1)
        map_y = random.randint(0, self.height-1)
        return (map_x, map_y)

    def showPlant(self, x, y):
        pos = None
        map_x, map_y = self.getMapIndex(x, y)
        if self.isValid(map_x, map_y) and self.isMovable(map_x, map_y):
            pos = self.getMapGridPos(map_x, map_y)
        return pos
