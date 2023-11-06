import pygame
from Shape import Shaper
import math
from NoteManager import NoteManager

class Note: # 충돌판정 여기서 
    def __init__(self, shaper: Shaper , screen: pygame.display, noteManager: NoteManager ,noteSpeed: int = 1):
        self.areaNum = -1
        self.vertex = [[0,0] for i in range(4)]
        self.noteSpeed = noteSpeed
        self.noteSize = 30
        self.shaper = shaper
        self.screen = screen
        self.isSpawned = False
        noteManager.LoadNotes(self)
        
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
            
        borderVectors[0][0] /= math.dist(self.shaper.centerPoint, borderCoords[0])
        borderVectors[0][1] /= math.dist(self.shaper.centerPoint, borderCoords[0])
        borderVectors[1][0] /= math.dist(self.shaper.centerPoint, borderCoords[0])
        borderVectors[1][1] /= math.dist(self.shaper.centerPoint, borderCoords[0])
        print(str(self.areaNum) + " " + str(borderVectors))
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
           
            pygame.draw.circle(screen ,(255,0,255), self.vertex[0], 10)
            pygame.draw.circle(screen ,(255,0,255), self.vertex[1], 10)
            pygame.draw.circle(screen ,(255,0,255), self.vertex[2], 10)
            pygame.draw.circle(screen ,(255,0,255), self.vertex[3], 10)
            
            self.isSpawned = True
            return self.vertex

    
    # 노트 각각에 대해서 작동. self.noteSpeed에 따라 네 점의 좌표 변화
    # 예외처리 > center좌표 도달하면 네 점 각각 모두 경우 체크하고 포지션 center로 고정.
    def MoveNote(self, borderCoords, screen: pygame.display): # 매 프레임마다 실행       
        if self.isSpawned:
            for vertex in self.vertex:
                if self.areaNum == 2:
                    pygame.draw.circle(screen, (255,0,255), vertex, 10)
                elif self.areaNum == 3:
                    pygame.draw.circle(screen, (0,0,255), vertex, 10)
                
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
            pygame.draw.polygon(screen,(255,255,255), [self.vertex[0],self.vertex[1], self.vertex[3], self.vertex[2]])

    def ReleaseNote(self, borderCoords, screen: pygame.display):
        if not self.IsNoteStandby():
            self.MakeNote(borderCoords, screen)
            self.MoveNote(borderCoords, screen)
        
    def IsNoteStandby(self):
        if self.areaNum == -1 or self.areaNum == 0:
            return True
        else:
            return False

    def NoteStandby(self):
        self.areaNum = -1
        self.isSpawned = False
        self.vertex = [[0,0] for i in range(4)]
        
    def ReadyNote(self, areaNum):
        self.areaNum = areaNum
        
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
        print(playerVec1Angle)
        
        playerVec1ProjDist = math.dist(self.vertex[2], playerPos) * math.cos(playerVec1Angle)    
        playerVec2ProjDist = math.dist(self.vertex[3], playerPos) * math.cos(playerVec2Angle)
        
        if(playerVec1ProjDist + playerVec2ProjDist) == math.dist(self.vertex[2], self.vertex[3]):
            return True
        else:
            return False
            
        
    def IsPlayerHit(self, playerPos):
        # distance = abs((self.vertex[3][0] - self.vertex[2][0]) * (self.vertex[2][1] - playerPos[1]) - (self.vertex[2][0] - playerPos[0]) * (self.vertex[3][1] - self.vertex[2][1]))
        # denominator = math.sqrt((self.vertex[3][0] - self.vertex[2][0]) ** 2 + (self.vertex[3][1] - self.vertex[2][1]) ** 2)
        # distance /= denominator
        # # if denominator > 0:
        # #     distance /= denominator
        # if distance <= 5:
        #     print("HITHITHITHITHITHITHIT")
        #     self.NoteStandby()
        #     return True
        # distance = abs((x2 - x1) * (y1 - y) - (x1 - x) * (y2 - y1)) / math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        vertexXPos = [self.vertex[0][0], self.vertex[1][0], self.vertex[2][0], self.vertex[3][0]]
        vertexYPos = [self.vertex[0][1], self.vertex[1][1], self.vertex[2][1], self.vertex[3][1]]
        vertexMinX, vertexMaxX = min(vertexXPos), max(vertexXPos)
        vertexMinY, vertexMaxY = min(vertexYPos), max(vertexYPos)
        if (playerPos[0] >= vertexMinX and playerPos[0] <= vertexMaxX) and (playerPos[1] >= vertexMinY and playerPos[1] <= vertexMaxY):
            return True
        else:
            return False

    def NoteHitShaper(self):
        shaperLine = math.dist(self.shaper.points[0], self.shaper.points[1])
        if int(shaperLine) >= int(math.dist(self.vertex[2], self.vertex[3])):
            print("OK")
            self.NoteStandby()
            return True
        else:
            return False # 2가 작은 인덱스, 3이 큰 인덱스   

    # -----Called by LevelManager-----
    #def LoadNote(self):
    def ResetNote(self):
        self.NoteStandby()
        