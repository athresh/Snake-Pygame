# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 17:01:52 2017

@author: Athresh
"""
from itertools import cycle
import random
import sys

import pygame
import win32con
from pygame.locals import *
import collections
import copy

import win32gui
import win32ui

FPS = 30
SCREENWIDTH  = 260
SCREENHEIGHT = 260
startX = 91
startY = 91
gameoverX = 10
gameoverY = 10

#Initializing parameters
InitSnakeL = 3
snakeList = {}
IMAGE = {}
move = 0
maxscore = 0
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

def screenshot():
    hwnd = 0
    w = 800
    h = 800
    #hwnd = win32gui.FindWindow(None, windowname)
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)
    
    bmpfilename = 'Screenshot' + 'GameComplete' + '.png'
    dataBitMap.SaveBitmapFile(cDC, bmpfilename)
    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

def ShowGameOverScreen():
    global gameover
    SCREEN.blit(IMAGE['gameover'], (gameoverX,gameoverY))
    pygame.display.update()
    FPSCLOCK.tick(FPS)
    gameover = 1

def GenerateNewFood():
    global foodPos,mat,move
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
        head = (prevHead[0],prevHead[1]-move)
        snakeQ.append(head)
        if head != foodPos:    
            tail = snakeQ.popleft()
        lastKey = 'left'
        updated = 1
        
    if direction == 'right' and lastKey!='left':
        prevHead = snakeQ.pop()
        snakeQ.append(prevHead)
        head = (prevHead[0],prevHead[1]+move)
        snakeQ.append(head)
        if head != foodPos:    
            tail = snakeQ.popleft()
        lastKey = 'right'
        updated = 1
    
    if direction == 'up' and lastKey!='down':
        prevHead = snakeQ.pop()
        snakeQ.append(prevHead)
        head = (prevHead[0]-move,prevHead[1])
        snakeQ.append(head)
        if head != foodPos:    
            tail = snakeQ.popleft()
        lastKey = 'up'
        updated = 1
        
    if direction == 'down' and lastKey!='up':
        prevHead = snakeQ.pop()
        snakeQ.append(prevHead)
        head = (prevHead[0]+move,prevHead[1])
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
        head = (startX-(InitSnakeL - i)*move,startY)
        snakeQ.append(head)
        SCREEN.blit(IMAGE['snake'], head)
        mat[head[1]][head[0]] = 1
    pygame.display.update()
    FPSCLOCK.tick(FPS)
        

def FindShortestPath(snakePos,foodPos):
    global mat,snakeQ
    #mat2 = [[mat[y][x] for x in range(SCREENWIDTH+move)] for y in range(SCREENHEIGHT+move)]
    snakeQ2 = copy.deepcopy(snakeQ)
    mat2 = copy.deepcopy(mat)
    checkedMat = [[1000 for x in range(SCREENWIDTH+move)] for y in range(SCREENHEIGHT+move)]
    PathQ = collections.deque()
    Q = collections.deque()
    pos = (snakePos[0],snakePos[1],0)
    Q.append(pos)
    checkedMat[pos[1]][pos[0]] = 0
    dist = 0
    foodFound = 0
    while(Q):
        pos = Q.popleft()
        #print('pos0= ',pos[0],' pos1= ',pos[1])
        if pos[0]+move<SCREENHEIGHT:
            #check tile below
            #print('down')
            posNew = (pos[0]+move,pos[1],pos[2]+1)
            if mat2[posNew[1]][posNew[0]]==0 and checkedMat[posNew[1]][posNew[0]]==1000:
                Q.append(posNew)
                checkedMat[posNew[1]][posNew[0]]=min((checkedMat[posNew[1]][posNew[0]],posNew[2]))
            if posNew[0]==foodPos[0] and posNew[1]==foodPos[1]:
                foodFound = 1
                break
            
            
        if pos[0]-move>=0:
            #check tile above
            #print('up')
            posNew = (pos[0]-move,pos[1],pos[2]+1)
            if mat2[posNew[1]][posNew[0]]==0 and checkedMat[posNew[1]][posNew[0]]==1000:
                Q.append(posNew)
                checkedMat[posNew[1]][posNew[0]]=min((checkedMat[posNew[1]][posNew[0]],posNew[2]))
            if posNew[0]==foodPos[0] and posNew[1]==foodPos[1]:
                foodFound = 1
                break
            
            
        if pos[1]+move<SCREENWIDTH:
            #check tile right
            #print('right')
            posNew = (pos[0],pos[1]+move,pos[2]+1)
            if mat2[posNew[1]][posNew[0]]==0 and checkedMat[posNew[1]][posNew[0]]==1000:
                Q.append(posNew)
                checkedMat[posNew[1]][posNew[0]]=min((checkedMat[posNew[1]][posNew[0]],posNew[2]))
            if posNew[0]==foodPos[0] and posNew[1]==foodPos[1]:
                foodFound = 1
                break
        
        
            
        if pos[1]-move>=0:
            #check tile left
            #print('left')
            posNew = (pos[0],pos[1]-move,pos[2]+1)
            if mat2[posNew[1]][posNew[0]]==0 and checkedMat[posNew[1]][posNew[0]]==1000:
                Q.append(posNew)
                checkedMat[posNew[1]][posNew[0]]=min((checkedMat[posNew[1]][posNew[0]],posNew[2]))
            if posNew[0]==foodPos[0] and posNew[1]==foodPos[1]:
                foodFound = 1
                break
        
        if dist < posNew[2]:
            dist = posNew[2]
            if(snakeQ2):
                snakeTail = snakeQ2.popleft()
                mat2[snakeTail[1]][snakeTail[0]]==0
    
    #traverse downhill from destination to source
    if foodFound == 0:
        ShowGameOverScreen()
        return -1
    x = foodPos[1]
    y = foodPos[0]
    minadj = checkedMat[x][y]
    PathQ.append((y,x))
    while(checkedMat[x][y]!=0):
        #print('tracing back')
        if x+move<SCREENHEIGHT:
            minadj = min((checkedMat[x+move][y],minadj))
            x2 = x+move
            y2 = y
        if x-move>=0:
            if checkedMat[x-move][y] < minadj:
                x2 = x-move
                y2 = y
            
        if y-move>=0:
            if checkedMat[x][y-move] < minadj:
                x2 = x
                y2 = y-move
        if y+move<SCREENWIDTH:
            if checkedMat[x][y+move] < minadj:
                x2 = x
                y2 = y+move
            
        x = x2
        y = y2
        minadj = min(minadj,checkedMat[x][y])
        if checkedMat[x][y]!=0:
            #print((y,x))
            PathQ.append((y,x))
        
    
    #print('length of PathQ = ',len(PathQ))
    return PathQ

def GetNextMove(nextPos,curSnakePos):
    if(nextPos[0]==curSnakePos[0]+move):
        return 'down'
    elif(nextPos[0]==curSnakePos[0]-move):
        return 'up'
    elif(nextPos[1]==curSnakePos[1]+move):
        return 'right'
    elif(nextPos[1]==curSnakePos[1]-move):
        return 'left'
    else:
        return 'None'

def MainGame():
    global lastKey, mat, snakeQ, gameover, tail, foodPos,updated,maxscore
    gameover = 0
    score = 0
    direction = ''
    snakeQ = collections.deque()
    mat = [[0 for x in range(SCREENWIDTH+move)] for y in range(SCREENHEIGHT+move)] 
    updated = 0
    lastKey = 'right'
    InitializeSnake()
    GenerateNewFood()
    PathQ = FindShortestPath((startX,startY),foodPos)
    while True:
        updated = 0
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                print('maxscore = ',maxscore)
                pygame.quit()
        curSnakePos = snakeQ.pop()
        snakeQ.append(curSnakePos)
        if PathQ:
            nextPos=PathQ.pop()
            direction = GetNextMove(nextPos,curSnakePos)
            updatePosition(direction)
        else:
            SCREEN.blit(IMAGE['freecell'], foodPos)
            GenerateNewFood()
            PathQ = FindShortestPath((startX,startY),foodPos)
        if gameover !=1 and updated == 1:
            addPosition = snakeQ.pop()
            snakeQ.append(addPosition)
            if addPosition != foodPos:
                SCREEN.blit(IMAGE['freecell'], tail)
            else:
                SCREEN.blit(IMAGE['freecell'], addPosition)
                score+=1
                maxscore = max(maxscore,score)
                if score>=(SCREENHEIGHT/13)*(SCREENWIDTH/13) - InitSnakeL:
                    screenshot()
                    ShowGameOverScreen()
                GenerateNewFood()
                PathQ = FindShortestPath(addPosition,foodPos)
            SCREEN.blit(IMAGE['snake'], addPosition)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
        if gameover == 1:
            break
    
    if gameover == 1:
        return
        
   
if __name__ == '__main__':
    main()