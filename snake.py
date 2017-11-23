# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 17:01:52 2017

@author: Athresh
"""
from itertools import cycle
import random
import sys

import pygame
from pygame.locals import *
import collections

FPS = 15
SCREENWIDTH  = 390
SCREENHEIGHT = 520
PlayAreaWidth = 288
PlayAreaHeight = 420
startX = 143
startY = 260
headX = startX
headY = startY
gameoverX = 10
gameoverY = 10
#foodStart = (144,311)
InitSnakeL = 5
snakeList = {}
IMAGE = {}
move = 0
#"C:/Users/Athresh/Documents/ATH ML/Python/Snake/assests/snake0.png"

def main():
    global SCREEN, FPSCLOCK,move,gameover
    
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Snake')
    
    while True:
        IMAGE['snake'] = pygame.image.load('assets/snake0.png').convert_alpha()
        IMAGE['gameover'] = pygame.image.load('assets/gameover.png').convert_alpha()
        IMAGE['background'] = pygame.image.load('assets/background.png').convert_alpha()
        IMAGE['food'] = pygame.image.load('assets/food.png').convert_alpha()
        IMAGE['freecell'] = pygame.image.load('assets/free cell.png').convert_alpha()
        move = IMAGE['snake'].get_height() + 1
        #SnakeImage = pygame.image.load(SNAKE).convert_alpha()
        MainGame()

def ShowGameOverScreen():
    global gameover
    SCREEN.blit(IMAGE['gameover'], (gameoverX,gameoverY))
    pygame.display.update()
    FPSCLOCK.tick(FPS)
    gameover = 1

def GenerateNewFood():
    global foodPos,mat
    foodPos = (random.randint(1,(SCREENWIDTH/move) - 1)*(move),random.randint(1,(SCREENHEIGHT/move) - 1)*(move))
    while mat[foodPos[1]][foodPos[0]] == 1:
        foodPos = (random.randint(1,(SCREENWIDTH/move) - 1)*move,random.randint(1,(SCREENHEIGHT/move) - 1)*move)
    SCREEN.blit(IMAGE['food'], foodPos)
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def OppositeDirection(drct):
    if drct == 'up':
        return 'down'
    elif drct == 'down':
        return 'up'
    elif drct == 'right':
        return 'left'
    elif drct == 'left':
        return 'right'
    else:
        return ''


def updatePosition(direction):
    global lastKey, mat, snakeQ, tail, foodPos,updated
    updated = 0
    if direction == 'left' and lastKey!='right':
        prevHead = snakeQ.pop()
        snakeQ.append(prevHead)
        head = (prevHead[0]-move,prevHead[1])
        snakeQ.append(head)
        if head != foodPos:    
            tail = snakeQ.popleft()
        lastKey = 'left'
        updated = 1
        
    if direction == 'right' and lastKey!='left':
        prevHead = snakeQ.pop()
        snakeQ.append(prevHead)
        head = (prevHead[0]+move,prevHead[1])
        snakeQ.append(head)
        if head != foodPos:    
            tail = snakeQ.popleft()
        lastKey = 'right'
        updated = 1
    
    if direction == 'up' and lastKey!='down':
        prevHead = snakeQ.pop()
        snakeQ.append(prevHead)
        head = (prevHead[0],prevHead[1]-move)
        snakeQ.append(head)
        if head != foodPos:    
            tail = snakeQ.popleft()
        lastKey = 'up'
        updated = 1
        
    if direction == 'down' and lastKey!='up':
        prevHead = snakeQ.pop()
        snakeQ.append(prevHead)
        head = (prevHead[0],prevHead[1]+move)
        snakeQ.append(head)
        if head != foodPos:    
            tail = snakeQ.popleft()
        lastKey = 'down'
        updated = 1
    
    if updated == 1:
        if head[1]>SCREENHEIGHT or head[0]>SCREENWIDTH or head[1]<0 or head[0]<0:
            ShowGameOverScreen()
        if mat[head[1]][head[0]] == 1:
            ShowGameOverScreen()
        else:
            mat[head[1]][head[0]] = 1
        if head != foodPos:
            mat[tail[1]][tail[0]] = 0

def InitializeSnake():
    global InitSnakeL,mat
    SCREEN.blit(IMAGE['background'], (0,0))
    for i in range(1,InitSnakeL+1):
        head = (headX-(InitSnakeL - i)*move,headY)
        snakeQ.append(head)
        SCREEN.blit(IMAGE['snake'], head)
        mat[head[1]][head[0]] = 1
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def MainGame():
    global lastKey, mat, snakeQ, gameover, tail, foodPos,updated
    gameover = 0
    score = 0
    spacePressed = 0
    direction = ''
    snakeQ = collections.deque()
    mat = [[0 for x in range(SCREENWIDTH+move)] for y in range(SCREENHEIGHT+move)] 
    lastKey = 'right'
    InitializeSnake()
    GenerateNewFood()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    direction = 'left'
                elif event.key == K_RIGHT:
                     direction = 'right'
                elif event.key == K_UP:
                    direction = 'up'
                elif event.key == K_DOWN:
                    direction = 'down'
        if direction!='':
            if direction == OppositeDirection(lastKey):
                direction = lastKey
            updatePosition(direction)
            if gameover !=1 and updated == 1:
                addPosition = snakeQ.pop()
                snakeQ.append(addPosition)
                if addPosition != foodPos:
                    SCREEN.blit(IMAGE['freecell'], tail)
                else:
                    SCREEN.blit(IMAGE['freecell'], addPosition)
                    score+=1
                    GenerateNewFood()
                SCREEN.blit(IMAGE['snake'], addPosition)
                pygame.display.update()
                FPSCLOCK.tick(FPS)
            if gameover == 1:
                break
        
   
if __name__ == '__main__':
    main()