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

import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import SGD


FPS = 100
SCREENWIDTH  = 260
SCREENHEIGHT = 260
startX = 91
startY = 91
gameoverX = 10
gameoverY = 10
InitSnakeL = 3
snakeList = {}
IMAGE = {}
move = 0
maxscore = 0
InitNumSnakes = 5
#"C:/Users/Athresh/Documents/ATH ML/Python/Snake/assests/snake0.png"

load_saved_pool = 1
save_current_pool = 1
current_pool = []
fitness = []
total_models = 50


# Initialize all models
for i in range(total_models):
    model = Sequential()
    model.add(Dense(output_dim=7, input_dim=3))
    model.add(Activation("sigmoid"))
    model.add(Dense(output_dim=1))
    model.add(Activation("sigmoid"))

    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss="mse", optimizer=sgd, metrics=["accuracy"])
    current_pool.append(model)
    fitness.append(-100)

for i in range(total_models):
    print(current_pool[i].get_weights())

def main():
    global SCREEN, FPSCLOCK,move,gameover
    
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Snake')
    
    while True:
        for i in range(0,InitNumSnakes):
            ImgName = 'snake' + str(i)
            fpath = 'assets/' + ImgName + '.png'
            IMAGE[ImgName] = pygame.image.load(fpath).convert_alpha()
        
        IMAGE['gameover'] = pygame.image.load('assets/gameover.png').convert_alpha()
        IMAGE['background'] = pygame.image.load('assets/background.png').convert_alpha()
        IMAGE['food'] = pygame.image.load('assets/food.png').convert_alpha()
        IMAGE['freecell'] = pygame.image.load('assets/free cell.png').convert_alpha()
        move = IMAGE['snake0'].get_height() + 1
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
    SCREEN.blit(IMAGE['background'], (0,0))
    SCREEN.blit(IMAGE['gameover'], (gameoverX,gameoverY))
    pygame.display.update()
    FPSCLOCK.tick(FPS)
    gameover = 1

def GenerateNewFood(SnakeIter):
    global foodPos,mat,move
    si = SnakeIter
    foodPos[si] = (random.randint(1,(SCREENWIDTH/move) - 1)*(move),random.randint(1,(SCREENHEIGHT/move) - 1)*(move))
    while mat[si][foodPos[si][1]][foodPos[si][0]] == 1:
        foodPos[si] = (random.randint(1,(SCREENWIDTH/move) - 1)*move,random.randint(1,(SCREENHEIGHT/move) - 1)*move)

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


def updatePosition(direction,SnakeIter):
    global lastKey, mat, snakeQ, tail, foodPos,updated, gameover
    si = SnakeIter
    updated[si] = 0
    if direction == 'left':
        prevHead = snakeQ[si].pop()
        snakeQ[si].append(prevHead)
        head = (prevHead[0],prevHead[1]-move)
        snakeQ[si].append(head)
        if head != foodPos[si]:    
            tail[si] = snakeQ[si].popleft()
        updated[si] = 1
        
    if direction == 'right':
        prevHead = snakeQ[si].pop()
        snakeQ[si].append(prevHead)
        head = (prevHead[0],prevHead[1]+move)
        snakeQ[si].append(head)
        if head != foodPos[si]:    
            tail[si] = snakeQ[si].popleft()
        updated[si] = 1
    
    if direction == 'up':
        prevHead = snakeQ[si].pop()
        snakeQ[si].append(prevHead)
        head = (prevHead[0]-move,prevHead[1])
        snakeQ[si].append(head)
        if head != foodPos[si]:    
            tail[si] = snakeQ[si].popleft()
        updated[si] = 1
        
    if direction == 'down':
        prevHead = snakeQ[si].pop()
        snakeQ[si].append(prevHead)
        head = (prevHead[0]+move,prevHead[1])
        snakeQ[si].append(head)
        if head != foodPos[si]:    
            tail[si] = snakeQ[si].popleft()
        updated[si] = 1
    
    if updated[si] == 1:
        if head[1]>SCREENHEIGHT or head[0]>SCREENWIDTH or head[1]<0 or head[0]<0:
            gameover[si] = 1
            #ShowGameOverScreen()
        if mat[si][head[1]][head[0]] == 1:
            gameover[si] = 1
            #ShowGameOverScreen()
        else:
            mat[si][head[1]][head[0]] = 1
        if head != foodPos[si]:
            mat[si][tail[si][1]][tail[si][0]] = 0

def InitializeSnake(numSnakes):
    global InitSnakeL,mat, snakeQ
    SCREEN.blit(IMAGE['background'], (0,0))
    for j in range(0,numSnakes):
        startX = random.randint(InitSnakeL,(SCREENWIDTH/move) - 1)*(move)
        startY = random.randint(InitSnakeL,(SCREENHEIGHT/move) - 1)*(move)
        sname = 'snake' + str(j)
        for i in range(1,InitSnakeL+1):
            head = (startX-(InitSnakeL - i)*move,startY)
            snakeQ[j].append(head)
            mat[j][head[1]][head[0]] = 1
        

def FindShortestPath(snakePos,foodPos,SnakeIter):
    global mat,snakeQ,gameover
    si = SnakeIter
    snakeQ2 = copy.deepcopy(snakeQ[si])
    mat2 = copy.deepcopy(mat[si])
    checkedMat = [[1000 for x in range(SCREENWIDTH+move)] for y in range(SCREENHEIGHT+move)]
    PathQ = collections.deque()
    Q = collections.deque()
    pos = (snakePos[0],snakePos[1],0)
    Q.append(pos)
    checkedMat[pos[1]][pos[0]] = 0
    dist = 0
    foodFound = 0
    foodposlcl = foodPos[si]
    while(Q):
        pos = Q.popleft()
        if pos[0]+move<SCREENHEIGHT:
            #check tile below
            posNew = (pos[0]+move,pos[1],pos[2]+1)
            if mat2[posNew[1]][posNew[0]]==0 and checkedMat[posNew[1]][posNew[0]]==1000:
                Q.append(posNew)
                checkedMat[posNew[1]][posNew[0]]=min((checkedMat[posNew[1]][posNew[0]],posNew[2]))
            if posNew[0]==foodposlcl[0] and posNew[1]==foodposlcl[1]:
                foodFound = 1
                break
            
            
        if pos[0]-move>=0:
            #check tile above
            posNew = (pos[0]-move,pos[1],pos[2]+1)
            if mat2[posNew[1]][posNew[0]]==0 and checkedMat[posNew[1]][posNew[0]]==1000:
                Q.append(posNew)
                checkedMat[posNew[1]][posNew[0]]=min((checkedMat[posNew[1]][posNew[0]],posNew[2]))
            if posNew[0]==foodposlcl[0] and posNew[1]==foodposlcl[1]:
                foodFound = 1
                break
            
            
        if pos[1]+move<SCREENWIDTH:
            #check tile right
            posNew = (pos[0],pos[1]+move,pos[2]+1)
            if mat2[posNew[1]][posNew[0]]==0 and checkedMat[posNew[1]][posNew[0]]==1000:
                Q.append(posNew)
                checkedMat[posNew[1]][posNew[0]]=min((checkedMat[posNew[1]][posNew[0]],posNew[2]))
            if posNew[0]==foodposlcl[0] and posNew[1]==foodposlcl[1]:
                foodFound = 1
                break
        
        
            
        if pos[1]-move>=0:
            #check tile left
            posNew = (pos[0],pos[1]-move,pos[2]+1)
            if mat2[posNew[1]][posNew[0]]==0 and checkedMat[posNew[1]][posNew[0]]==1000:
                Q.append(posNew)
                checkedMat[posNew[1]][posNew[0]]=min((checkedMat[posNew[1]][posNew[0]],posNew[2]))
            if posNew[0]==foodposlcl[0] and posNew[1]==foodposlcl[1]:
                foodFound = 1
                break
        
        if dist < posNew[2]:
            dist = posNew[2]
            if(snakeQ2):
                snakeTail = snakeQ2.popleft()
                mat2[snakeTail[1]][snakeTail[0]]==0
    
    #traverse downhill from destination to source
    if foodFound == 0:
        gameover[si] = 1
        #ShowGameOverScreen()
        return -1
    x = foodposlcl[1]
    y = foodposlcl[0]
    minadj = checkedMat[x][y]
    PathQ.append((y,x))
    while(checkedMat[x][y]!=0):
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
            PathQ.append((y,x))
        
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

def KillSnake(SnakeIter):
    global snakeQ,mat
    si = SnakeIter
    while(snakeQ[si]):
        head = snakeQ[si].pop()
        mat[si][head[1]][head[0]] = 0

def InitializeNewSnake(SnakeIter):
    global mat, snakeQ, InitSnakeL
    si = SnakeIter
    startX = random.randint(InitSnakeL,(SCREENWIDTH/move) - 1)*(move)
    startY = random.randint(InitSnakeL,(SCREENHEIGHT/move) - 1)*(move)
    while startX==foodPos[si][0] and startY==foodPos[si][1]:
        startX = random.randint(InitSnakeL,(SCREENWIDTH/move) - 1)*(move)
        startY = random.randint(InitSnakeL,(SCREENHEIGHT/move) - 1)*(move)
    for i in range(1,InitSnakeL+1):
        head = (startX-(InitSnakeL - i)*move,startY)
        snakeQ[si].append(head)
        mat[si][head[1]][head[0]] = 1

def loadscreen(numsn):
    global foodPos,snakeQ
    snq = copy.deepcopy(snakeQ)
    SCREEN.blit(IMAGE['background'],(0,0))
    for i in range(0,numsn):
        fpos = foodPos[i]
        SCREEN.blit(IMAGE['food'], fpos)
        sname = 'snake' + str(i)
        while(snq[i]):
            spos = snq[i].pop()
            SCREEN.blit(IMAGE[sname], spos)

def MainGame():
    global lastKey, gameover, foodPos,updated,maxscore, tail, mat, snakeQ
    direction = ''
    updated,gameover,mat,snakeQ,tail,PathQ,foodPos = {},{},{},{},{},{},{}

    NumSnakes = InitNumSnakes
    for i in range(0,InitNumSnakes):
        gameover[i] = 0
        updated[i] = 0
        snakeQ[i] = collections.deque()
        PathQ[i] = collections.deque()
        mat[i] = [[0 for x in range(SCREENWIDTH+move)] for y in range(SCREENHEIGHT+move)]
    InitializeSnake(InitNumSnakes)
    for i in range(0,InitNumSnakes):
        GenerateNewFood(i)
    for i in range(0,InitNumSnakes):
        head = snakeQ[i].pop()
        snakeQ[i].append(head)
        PathQ[i] = FindShortestPath(head,foodPos,i)
    
    loadscreen(NumSnakes)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
        for i in range(0,NumSnakes):
            gameover[i] = 0
            curSnakePos = snakeQ[i].pop()
            snakeQ[i].append(curSnakePos)
            if PathQ[i]:
                nextPos=PathQ[i].pop()
                direction = GetNextMove(nextPos,curSnakePos)
                updatePosition(direction,i)

            if gameover[i] !=1 and updated[i] == 1:
                addPosition = snakeQ[i].pop()
                snakeQ[i].append(addPosition)
                
                if addPosition == foodPos[i]:
                    
                    GenerateNewFood(i)
                    PathQ[i] = FindShortestPath(addPosition,foodPos,i)
                    if gameover[i]==0:
                        ps = PathQ[i].popleft()
                        PathQ[i].appendleft(ps)

            if gameover[i]==1:
                KillSnake(i)
                InitializeNewSnake(i)
                addPosition = snakeQ[i].pop()
                snakeQ[i].append(addPosition)
                PathQ[i] = FindShortestPath(addPosition,foodPos,i)
                    
        loadscreen(NumSnakes)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

        
   
if __name__ == '__main__':
    main()