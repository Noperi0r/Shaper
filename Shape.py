import pygame
import math

class Shaper():
    def __init__(self, centerPoint: list, n=6, radius=100):
        self.n = n
        self.centerPoint = centerPoint
        self.points = [[0,0] for i in range (self.n)] # n개 포인트 필요
        self.radius = radius
        self.eachAngle = (360 / self.n) * math.pi / 180.0 # ex n이 6이면 60도

        self.playerRoutePoint = [[0,0] for i in range (0, self.n)]
        

    def MakeNPoints(self, screen: pygame.display, n): # n개의 points 생성
        self.n = n
        for i in range (self.n):
                angle = self.eachAngle * i
                x = self.centerPoint[0] + self.radius * math.cos(angle)                        
                y = self.centerPoint[1] + self.radius * math.sin(angle)                     
                self.points[i] = [x,y]   
                # print(self.points[i]) # test
                # pygame.draw.circle(screen,(255,255,0),self.points[i], 10)
                
                outerX = self.centerPoint[0] + (self.radius+25) * math.cos(angle) # radius + value 수정 시 Player.py playerradius도 동기화 필요
                outerY = self.centerPoint[1] + (self.radius+25) * math.sin(angle)                    
                self.playerRoutePoint[i] = [outerX, outerY]
                # 외곽선 +는 현재 25. Player radius + a 에서 a는 현재 10 
                
    # 이거 그냥 나중에 draw.polygon으로 변경            
    def MakeShapeLines(self, screen: pygame.display):
        for i in range(self.n):
            if i == 0:
                pygame.draw.line(screen, (255, 255, 0), self.points[i],self.points[self.n-1], 10)
            else:
                pygame.draw.line(screen, (255, 255, 0), self.points[i-1],self.points[i], 10)
                
    def DiscernNoteArea(self, screen: pygame.display, length = 600):
        noteCoordinates = [[0,0] for i in range(self.n)]
        for i in range(self.n):
            angle = self.eachAngle * i
            x = self.centerPoint[0] + length * math.cos(angle)
            y = self.centerPoint[1] + length * math.sin(angle)
            noteCoordinates[i] = [x,y]
            pygame.draw.line(screen, (255, 0, 0), self.centerPoint , [x, y], 5)
            pygame.draw.circle(screen, (255,255,255), [x,y], 10)
        return noteCoordinates # n 6 이면 6개의 좌표 반환
    
    # ----- LevelManager 관련 -----
    def LoadShaper(self, screen:pygame.display, n: int): # 그 레벨 시작할 때 도형 생성하는거 여기로 옮겨줘야 함
        self.n = n           # 원래 만들었던 코드는 백업, 이 방법 망하면 원래 썼던 코드 써야할 수 있음 
        self.MakeNPoints(screen)
        self.MakeShapeLines(screen)
        
    #def ResetShaper(self): # 레벨 종료 아니면 게임 오버될 때 도형 삭제하는거 여기로 옮겨줘야 함
            

        
        