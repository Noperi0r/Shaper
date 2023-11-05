import pygame
from Shape import Shaper
import math

class Note: # 충돌판정 여기서 
    def __init__(self, shaper: Shaper , screen: pygame.display, noteSpeed: int = 5):
        self.areaNum = -1
        self.vertex = [[0,0] for i in range(4)]
        self.noteSpeed = noteSpeed
        self.noteSize = 30
        self.shaper = shaper
        self.screen = screen
        self.isSpawned = False
    
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
            pygame.draw.circle(screen ,(255,200,255), self.vertex[0], 10)
            pygame.draw.circle(screen ,(255,200,255), self.vertex[1], 10)
            pygame.draw.circle(screen ,(255,200,255), self.vertex[2], 10)
            pygame.draw.circle(screen ,(255,200,255), self.vertex[3], 10)
            
            self.isSpawned = True
            return self.vertex

    
    # 노트 각각에 대해서 작동. self.noteSpeed에 따라 네 점의 좌표 변화
    # 예외처리 > center좌표 도달하면 네 점 각각 모두 경우 체크하고 포지션 center로 고정.
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
        
    def IsPlayerHit(self, playerPos):
        distance = abs((self.vertex[3][0] - self.vertex[2][0]) * (self.vertex[2][1] - playerPos[1]) - (self.vertex[2][0] - playerPos[0]) * (self.vertex[3][1] - self.vertex[2][1]))
        distance /= math.sqrt((self.vertex[3][0] - self.vertex[2][0]) ** 2 + (self.vertex[3][1] - self.vertex[2][1]) ** 2)
        if distance <= 10:
            print("HITHITHITHITHITHITHIT")
            self.areaNum = -1
            return True

    # distance = abs((x2 - x1) * (y1 - y) - (x1 - x) * (y2 - y1)) / math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    