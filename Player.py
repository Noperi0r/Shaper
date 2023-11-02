import pygame
from Shape import Shaper
from math import dist

class Player(): 
    # Init 순서는 Shaper가 먼저 이루어져야 함 
    def __init__(self, shaper: Shaper): 
        self.shaper = shaper # 상속 말고, 변수로 Shape 가져야 함.
        self.velocity = 1
        self.playerRadius = shaper.radius + 10 
        self.playerPos = [shaper.centerPoint[0], shaper.centerPoint[1] + self.playerRadius]
        self.n = self.shaper.n
        self.shapeLength = dist(shaper.points[0], shaper.points[1]) 

    def Spawn(self, surface : pygame.display ):
        pygame.draw.circle(surface, (255,255,255), self.playerPos, 10)

    def GetPlayerRoutePoints(self): # !!. 비율 안 맞긴 함
        return self.shaper.playerRoutePoint
    
    def GetNearRoutePoints(self): # !!. 선분에 있을 때는 일단 판정 가능
        routePoints = self.GetPlayerRoutePoints()
        availablePoints = [] 
        for i in range(0, self.n):
            if  dist(routePoints[i], self.playerPos) <= self.shapeLength and len(availablePoints) < 2: # !! = 고려 필요? 
                availablePoints.append(routePoints[i]) # 0부터 n-1까지 loop 순서대로 가므로, 추가되는 것은 작은 index 순.
        if len(availablePoints) == 2:
            return availablePoints
        else: 
            print("RouteNumber Error")
            return []
            
    def GetRouteSlope(self):
        if len(self.GetNearRoutePoints()) == 2:
            nearRoutePoints = self.GetNearRoutePoints() # 세로 직선인 경우 처리 필요. 가로 직선인 경우 처리 필요
            
            if (nearRoutePoints[1][1] - nearRoutePoints[0][1]) == 0 or (nearRoutePoints[1][0] - nearRoutePoints[0][0]) == 0: # 가로 직선 
                return 1; # 값 뭐 줘야하지? 기본값? 
            else:
                return abs((nearRoutePoints[1][1] - nearRoutePoints[0][1]) / (nearRoutePoints[1][0] - nearRoutePoints[0][0]))
        else:
            print("Near points number Error")
            
            
    def Move(self, keys: pygame.key):
        # Precondition: 클래스 외부에서 L arrow, R arrow에 대한 입력에 대해서만 해당 함수 실행         
        # 위치 변경 
        slope = self.GetRouteSlope()
        # if slope == 0:
            
        
        # if keys == pygame.K_RIGHT: # clockwise 
        # else: # K left. Counter Clockwise 
            

        # draw
