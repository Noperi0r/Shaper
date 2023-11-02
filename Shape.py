import pygame
import math

class Shaper():
    def __init__(self, centerPoint : list, n=6, radius=100):
        self.n = n
        self.centerPoint = centerPoint
        self.points = [[0,0] for i in range (0, self.n)] # n개 포인트 필요
        self.radius = radius
        self.eachAngle = (360 / self.n) * math.pi / 180.0 # ex n이 6이면 60도

        self.playerRoutePoint = [[0,0] for i in range (0, self.n)]
        

    def MakeNPoints(self, screen: pygame.display): # n개의 points 생성
        for i in range (0, self.n):
                angle = self.eachAngle * i
                x = self.centerPoint[0] + self.radius * math.cos(angle)                        
                y = self.centerPoint[1] + self.radius * math.sin(angle)                     
                self.points[i] = [x,y]   
                print(self.points[i]) # test
                pygame.draw.circle(screen,(255,255,0),self.points[i], 15)
                
                outerX = self.centerPoint[0] + (self.radius+1) * math.cos(angle) # radius + value 수정 시 Player.py playerradius도 동기화 필요
                outerY = self.centerPoint[1] + (self.radius+10) * math.sin(angle)                    
                self.playerRoutePoint[i] = [outerX, outerY]
                
                
    def MakeShapeLines(self, screen: pygame.display):
        for i in range(0, self.n):
            if i == 0:
                pygame.draw.line(screen, (255, 255, 0), self.points[i],self.points[self.n-1], 10)
            else:
                pygame.draw.line(screen, (255, 255, 0), self.points[i-1],self.points[i], 10)
                
    def DrawNoteArea(self, screen: pygame.display, length = 300):
        for i in range(0, self.n):
            angle = self.eachAngle * i
            x = self.centerPoint[0] + length * math.cos(angle)
            y = self.centerPoint[1] + length * math.sin(angle)
            pygame.draw.line(screen, (255, 0, 0), self.centerPoint , [x, y], 5)
    
    
    
            

        
        