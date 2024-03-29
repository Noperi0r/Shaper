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
        
        self.shapeColor = [255,255,255]
        self.shapeLineColor = [0,0,0]
        self.borderLineColor = [255,255,255]

    def MakeNPoints(self, screen: pygame.display, n: int): # n개의 points 생성
        if self.n != n:
            self.n = n
            self.eachAngle = (360 / self.n) * math.pi / 180.0 # ex n이 6이면 60도
            self.points = [[0,0] for i in range(self.n)]
            self.playerRoutePoint = [[0,0] for i in range(self.n)]
        
        for i in range (self.n):
            angle = self.eachAngle * i
            x = self.centerPoint[0] + self.radius * math.cos(angle)                        
            y = self.centerPoint[1] + self.radius * math.sin(angle)       
            self.points[i] = [x,y]   
            outerX = self.centerPoint[0] + (self.radius+15) * math.cos(angle) # radius + value 수정 시 Player.py playerradius도 동기화 필요
            outerY = self.centerPoint[1] + (self.radius+15) * math.sin(angle)      
            self.playerRoutePoint[i] = [outerX, outerY]              
            #self.playerRoutePoint[i] = [outerX, outerY]
            # 외곽선 +는 현재 25. Player radius + a 에서 a는 현재 10 
        # self.points = points
        # self. playerRoutePoint = playerRoutePoint
        
    # 이거 그냥 나중에 draw.polygon으로 변경            
    def MakeShapeLines(self, screen: pygame.display, stage: int):
        if stage == 1:
            self.shapeColor = [253, 183, 185]
            self.shapeLineColor = [193, 119, 121]
        elif stage == 2:
            self.shapeColor = [155, 168, 174]
            self.shapeLineColor = [112, 122, 126]
        elif stage == 3:
            self.shapeColor = [238,169,144]
            self.shapeLineColor = [170,111,115]
        
        pygame.draw.polygon(screen, self.shapeColor, self.points)
        for i in range(self.n):
            if i == 0:
                pygame.draw.line(screen, self.shapeLineColor, self.points[i],self.points[self.n-1], 10)
            else:
                pygame.draw.line(screen, self.shapeLineColor, self.points[i-1],self.points[i], 10)
                
    def DiscernNoteArea(self, screen: pygame.display, length:int, stage: int):
        noteCoordinates = [[0,0] for i in range(self.n)]
        if stage==1:
            self.borderLineColor = [193, 119, 121]
        elif stage==2:
            self.borderLineColor = [112, 122, 126]
        elif stage==3:
            self.borderLineColor = [170,111,115]
        
        for i in range(self.n):
            angle = self.eachAngle * i
            x = self.centerPoint[0] + length * math.cos(angle)
            y = self.centerPoint[1] + length * math.sin(angle)
            noteCoordinates[i] = [x,y]
            pygame.draw.line(screen, self.borderLineColor, self.centerPoint , [x, y], 3)
            pygame.draw.circle(screen, (255,255,255), [x,y], 10)
        return noteCoordinates # n 6 이면 6개의 좌표 반환
    
    # ----- LevelManager 관련 -----
    def LoadShaper(self, screen:pygame.display, n: int): # 그 레벨 시작할 때 도형 생성하는거 여기로 옮겨줘야 함
        self.n = n           # 원래 만들었던 코드는 백업, 이 방법 망하면 원래 썼던 코드 써야할 수 있음 
        self.MakeNPoints(screen)
        self.MakeShapeLines(screen)
        
    #def ResetShaper(self): # 레벨 종료 아니면 게임 오버될 때 도형 삭제하는거 여기로 옮겨줘야 함
        
    def RotateShaper(self, angle):
        radAngle = math.radians(angle)
        newPoints = []
        for point in self.points:
            point[0] = self.centerPoint[0] + self.radius * math.cos(radAngle)
            point[1] = self.centerPoint[1] + self.radius * math.sin(radAngle)
                        