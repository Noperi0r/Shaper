import pygame
from Shape import Shaper
import math
#from NoteManager import NoteManager
from Player import Player

class Note: # 충돌판정 여기서 
    def __init__(self, shaper: Shaper , screen: pygame.display, noteSpeed: float=8):
        self.areaNum = -1
        self.vertex = [[0,0] for i in range(4)]
        self.noteSpeed = noteSpeed
        self.noteSize = 40
        self.shaper = shaper
        self.screen = screen
        self.isSpawned = False
        #noteManager.LoadNotes(self)
        self.spawnTime = -1
        
        self.stage = 0
        
    def GetAreaNum(self):
        return self.areaNum
    
    def GetAreaBorderVectors(self, borderCoords): # 6각형인 경우 6개의 경계벡터 도출
        # 이것도 player의 GetPlayerRoutePoints처럼 인덱스 작은 순대로 저장
        # self.areaNum은 0말고 1부터 시작해야 됨 
        if self.areaNum > self.shaper.n: 
            print("Area Number Error")
            return -1 
        
        borderVectors = [[0,0],[0,0]]
        # borderCoords = self.shaper.DiscernNoteArea(self.screen) # !! length 아직 미설정
        
        if self.areaNum == self.shaper.n:
            borderVectors[0][0] = self.shaper.centerPoint[0] - borderCoords[0][0]
            borderVectors[0][1] = self.shaper.centerPoint[1] - borderCoords[0][1]
            borderVectors[1][0] = self.shaper.centerPoint[0] - borderCoords[self.areaNum-1][0]
            borderVectors[1][1] = self.shaper.centerPoint[1] - borderCoords[self.areaNum-1][1]
            
        else:
            borderVectors[0][0] = self.shaper.centerPoint[0] - borderCoords[self.areaNum-1][0]
            borderVectors[0][1] = self.shaper.centerPoint[1] - borderCoords[self.areaNum-1][1]
            borderVectors[1][0] = self.shaper.centerPoint[0] - borderCoords[self.areaNum][0]
            borderVectors[1][1] = self.shaper.centerPoint[1] - borderCoords[self.areaNum][1] 
            
        borderVectors[0][0] /= math.dist(self.shaper.centerPoint, borderCoords[0]) # x
        borderVectors[0][1] /= math.dist(self.shaper.centerPoint, borderCoords[0]) # y
        borderVectors[1][0] /= math.dist(self.shaper.centerPoint, borderCoords[0]) # x
        borderVectors[1][1] /= math.dist(self.shaper.centerPoint, borderCoords[0]) # y

        return borderVectors
    
    def GetAreaBorderPoints(self, borderCoords): # n개 borderCoord에서 
        if self.areaNum > self.shaper.n: 
            print("Area Number Error")
            return -1 
        elif self.areaNum == self.shaper.n:
            return [borderCoords[0], borderCoords[self.areaNum-1]]
        else:
            return [borderCoords[self.areaNum-1], borderCoords[self.areaNum]]

    # 노트 네 점의 좌표 필요. 
    #노트의 네 가지 좌표 도출 > draw.polygon > 네 좌표 리스트 반환
    def MakeNote(self, borderCoords, screen: pygame.display): # 노트 초기 위치에서 생성
        if not self.isSpawned:
            if self.areaNum > self.shaper.n: 
                print("Area Number Error")
                return -1 
            noteVectors = [[0,0], [0,0]]
            
            self.vertex[0] = self.GetAreaBorderPoints(borderCoords)[0] # 두 포인트 반환 
            self.vertex[1] = self.GetAreaBorderPoints(borderCoords)[1] # 두 포인트 반환 
            noteVectors = self.GetAreaBorderVectors(borderCoords)
            
            self.vertex[2][0] = self.vertex[0][0] + self.noteSize * noteVectors[0][0]
            self.vertex[2][1] = self.vertex[0][1] + self.noteSize * noteVectors[0][1]
            
            self.vertex[3][0] = self.vertex[1][0] + self.noteSize * noteVectors[1][0]
            self.vertex[3][1] = self.vertex[1][1] + self.noteSize * noteVectors[1][1]
            
            pygame.draw.polygon(screen,(255,255,255), [self.vertex[0],self.vertex[1], self.vertex[3], self.vertex[2]])
           
            # pygame.draw.circle(screen ,(255,0,255), self.vertex[0], 10)
            # pygame.draw.circle(screen ,(255,0,255), self.vertex[1], 10)
            # pygame.draw.circle(screen ,(255,0,255), self.vertex[2], 10)
            # pygame.draw.circle(screen ,(255,0,255), self.vertex[3], 10)
            
            self.isSpawned = True
            return self.vertex

    
    # 노트 각각에 대해서 작동. self.noteSpeed에 따라 네 점의 좌표 변화
    # 예외처리 > center좌표 도달하면 네 점 각각 모두 경우 체크.
    def MoveNote(self, borderCoords, screen: pygame.display): # 매 프레임마다 실행       
        if self.isSpawned:
            noteVectors = self.GetAreaBorderVectors(borderCoords) # 두 벡터 저장하는 2차원 배열
            
            for i in range(4):
                if (i % 2) ==0: #0번, 2번 인덱스 
                    self.vertex[i][0] += self.noteSpeed * noteVectors[0][0]
                    self.vertex[i][1] += self.noteSpeed * noteVectors[0][1]
                
                else: # 1번, 3번 인덱스
                    self.vertex[i][0] += self.noteSpeed * noteVectors[1][0]
                    self.vertex[i][1] += self.noteSpeed * noteVectors[1][1]
            
            if math.dist(self.vertex[2], self.shaper.centerPoint) <= 1:
                self.NoteStandby()
                print("RESET")
            
            return pygame.draw.polygon(screen,(255,255,255), [self.vertex[0],self.vertex[1], self.vertex[3], self.vertex[2]])
            
    def DeployNote(self, borderCoords, screen: pygame.display, deltaTime, player: Player):
        if not self.IsNoteStandby(deltaTime):
            self.MakeNote(borderCoords, screen)
            self.MoveNote(borderCoords, screen)
            #if self.MoveNote(borderCoords, screen).collidepoint(pygame.math.Vector2(playerPos[0], playerPos[1])):
            if self.stage == 3:
                if self.IsPlayerHitStage3(player.playerPos):   
                    player.playerDead = True
                    pygame.draw.polygon(screen,(255,0,0), [self.vertex[0],self.vertex[1], self.vertex[3], self.vertex[2]])
            else:
                if self.IsPlayerHit(player.playerPos):
                    player.playerDead = True
                    pygame.draw.polygon(screen,(255,0,0), [self.vertex[0],self.vertex[1], self.vertex[3], self.vertex[2]])

            if self.NoteHitShaper():
                self.NoteStandby()
        
    def IsNoteStandby(self, deltaTime):
        if self.areaNum == -1 or self.areaNum == 0:
            return True
        else:
            if self.spawnTime > 0:
                self.spawnTime -= deltaTime # spawnTime은 readyNote에서 설정
                return True
            else:
                return False

    def NoteStandby(self):
        self.areaNum = -1
        self.isSpawned = False
        self.vertex = [[0,0] for i in range(4)]
        
    def ReadyNote(self, areaNum, spawnTime):
        self.areaNum = areaNum
        self.spawnTime = spawnTime
        
    def IsPlayerInArea(self, playerPos):
        notePlaneVec = [0,0]
        notePlaneVec[0] = self.vertex[2][0] - self.vertex[3][0] 
        notePlaneVec[1] = self.vertex[2][1] - self.vertex[3][1] 
        
        toPlayerVec1 = [0,0]
        toPlayerVec2 = [0,0]
        
        toPlayerVec1[0] = playerPos[0] - self.vertex[2][0]
        toPlayerVec1[1] = playerPos[1] - self.vertex[2][1]
        toPlayerVec2[0] = playerPos[0] - self.vertex[3][0]
        toPlayerVec2[1] = playerPos[1] - self.vertex[3][1]
        
        dx1 = toPlayerVec1[0] - notePlaneVec[0]
        dy1 = toPlayerVec1[1] - notePlaneVec[1]
        dx2 = toPlayerVec2[0] - notePlaneVec[0]
        dy2 = toPlayerVec2[1] - notePlaneVec[1]
        
        playerVec1Angle = math.atan2(dy1, dx1)
        playerVec2Angle = math.atan2(dy2, dx2)
        
    
        playerVec1ProjDist = math.dist(self.vertex[2], playerPos) * math.cos(playerVec1Angle)    
        playerVec2ProjDist = math.dist(self.vertex[3], playerPos) * math.cos(playerVec2Angle)
        
        if(playerVec1ProjDist + playerVec2ProjDist) == math.dist(self.vertex[2], self.vertex[3]):
            return True
        else:
            return False
            
        
    def IsPlayerHit(self, playerPos):

        lineVector = [self.vertex[3][0]-self.vertex[2][0], self.vertex[3][1]-self.vertex[2][1]]
        lineVecDist = math.dist(self.vertex[3], self.vertex[2])
        
        lineToPlyerVector = [playerPos[0]-self.vertex[2][0], playerPos[1]-self.vertex[2][1]]
        linetoPlayDist = math.dist(playerPos, self.vertex[2])
        
        dotProduct = lineVector[0]*lineToPlyerVector[0] + lineVector[1]*lineToPlyerVector[1]
    
        #-----------------------
        # lineVector2 = [self.vertex[1][0]-self.vertex[0][0], self.vertex[1][1]-self.vertex[0][1]]
        # lineVecDist2 = math.dist(self.vertex[1], self.vertex[0])
        
        # lineToPlyerVector2 = [playerPos[0]-self.vertex[1][0], playerPos[1]-self.vertex[1][1]]
        # linetoPlayDist2 = math.dist(playerPos, self.vertex[1])
        
        # dotProduct2 = lineVector2[0]*lineToPlyerVector2[0] + lineVector2[1]*lineToPlyerVector2[1]
        
        if lineVecDist == 0 or linetoPlayDist == 0:
            return
        # if lineVecDist2 == 0 or linetoPlayDist2 == 0:
        #     return
        
        dotProduct /= (lineVecDist * linetoPlayDist) 
        #dotProduct2 /= (lineVecDist2 * linetoPlayDist2)
        angle = math.acos(dotProduct)
        #angle2 = math.acos(dotProduct2)
        
        if angle <= 0.1 and angle >= -0.1:
        #if angle2 <= 0.5 and angle >= -0.5:
            return True
        else:
            return False
        
    def IsPlayerHitStage3(self, playerPos):
        vertexXPos = [self.vertex[0][0], self.vertex[1][0], self.vertex[2][0], self.vertex[3][0]]
        vertexYPos = [self.vertex[0][1], self.vertex[1][1], self.vertex[2][1], self.vertex[3][1]]
        vertexMinX, vertexMaxX = min(vertexXPos), max(vertexXPos)
        vertexMinY, vertexMaxY = min(vertexYPos), max(vertexYPos)
        if (playerPos[0] >= vertexMinX and playerPos[0] <= vertexMaxX) and (playerPos[1] >= vertexMinY and playerPos[1] <= vertexMaxY):
            return True
        else:
            return False
        
    def NoteHitShaper(self):
        #if self.GetStageNum() == 3:
            shaperLine = math.dist(self.shaper.points[0], self.shaper.points[1])
            if int(shaperLine) >= int(math.dist(self.vertex[2], self.vertex[3])):
                self.NoteStandby()
                return True
            else:
                return False # 2가 작은 인덱스, 3이 큰 인덱스   

    def GetStageNum(self, stage):
        self.stage = stage
        return self.stage
        
    
        