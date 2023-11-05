import pygame
from Shape import Shaper
import math


class Player(): 
    # Init 순서는 Shaper가 먼저 이루어져야 함 
    def __init__(self, shaper: Shaper): 
        self.shaper = shaper # 상속 말고, 변수로 Shape 가져야 함.
        self.speed = 8
        self.playerRadius = shaper.radius + 10 
        self.playerPos = [shaper.centerPoint[0], shaper.centerPoint[1] + self.playerRadius]
        self.playerPos = [self.shaper.playerRoutePoint[1][0], self.shaper.playerRoutePoint[1][1]]
        #self.shapeLength = math.dist(shaper.points[0], shaper.points[1]) 

    def DrawPlayer(self, surface: pygame.display ):
        pygame.draw.circle(surface, (255,255,255), self.playerPos, 10)

    def GetPlayerRoutePoints(self): # !!. 비율 안 맞긴 함
        return self.shaper.playerRoutePoint
    
    def GetNearRoutePoints(self, keys): # !!. 선분에 있을 때는 일단 판정 가능. 인접 두 점 리스트 반환
        routePoints = self.GetPlayerRoutePoints()
        availablePoints = [] 
        routeLength = math.dist(routePoints[0], routePoints[1])
        for i in range(self.shaper.n):
            if  math.dist(routePoints[i], self.playerPos) <= routeLength and len(availablePoints) < 2: # !! = 고려 필요? 
                availablePoints.append(routePoints[i]) # 0부터 n-1까지 loop 순서대로 가므로, 추가되는 것은 작은 index 순.
            if len(availablePoints) == 2:
                if i == (self.shaper.n -1): # 마지막 선분 영역에 대한 예외 처리 
                    availablePoints = [availablePoints[1], availablePoints[0]] 
                return availablePoints
            
        if len(availablePoints) == 1:
            idx = -1
            for point in routePoints:
                if point == availablePoints[0]:
                    print("OK, Let us get it: " + str(i))
                    idx = i
                    break     

            if keys[pygame.K_RIGHT]: # 5 >> 0 경우 예외 
                if idx == (self.shaper.n-1):
                    availablePoints.append(routePoints[0])     
                else:
                    availablePoints.append(routePoints[idx+1])
                self.playerPos = availablePoints[0]
            elif keys[pygame.K_LEFT]: # 0 >> 5 경우 예외 
                if idx == 0:
                    availablePoints.append(routePoints[(self.shaper.n - 1)])
                else:
                    availablePoints.append(routePoints[idx-1])
                    availablePoints = [availablePoints[1], availablePoints[0]]
                self.playerPos = availablePoints[1] 
            return availablePoints
            
        if len(availablePoints) != 2: 
            #print(str(availablePoints[0]) + " / " + str())
            print("RouteNumber Error: length = " + str(len(availablePoints)))
            return availablePoints
        
            
    def GetRouteSlope(self, routePoints: list):  
        # routePoints는 GetNearRoutePoints 반환값이어야 함.
        if len(routePoints) == 2:
            #nearRoutePoints = self.GetNearRoutePoints() # 세로 직선인 경우 처리 필요. 가로 직선인 경우 처리 필요
            if (routePoints[1][1] - routePoints[0][1]) == 0 or (routePoints[1][0] - routePoints[0][0]) == 0: # 가로 직선 
                return 0 # 값 뭐 줘야하지? 기본값? 
            else:
                return abs((routePoints[1][1] - routePoints[0][1]) / (routePoints[1][0] - routePoints[0][0]))
        else:
            print("Near points number Error")

            
    def Move(self, keys):
        # Precondition: 클래스 외부에서 L arrow, R arrow에 대한 입력에 대해서만 해당 함수 실행         
        nearRoutePoints = self.GetNearRoutePoints(keys)
        #routeLinearFuncY = self.MakeLinearFunc(nearRoutePoints)        

        dirVector = [0,0]
        if keys[pygame.K_RIGHT]: # clockwise             
            dirVector[0] = nearRoutePoints[1][0] - nearRoutePoints[0][0] # default: 시계방향
            dirVector[1] = nearRoutePoints[1][1] - nearRoutePoints[0][1] 
        elif keys[pygame.K_LEFT]: #K left. Counter Clockwise 
            dirVector[0] = nearRoutePoints[0][0] - nearRoutePoints[1][0] # default: 시계방향
            dirVector[1] = nearRoutePoints[0][1] - nearRoutePoints[1][1] 

        dirVector[0] /= math.dist(nearRoutePoints[1], nearRoutePoints[0]) # Normalize
        dirVector[1] /= math.dist(nearRoutePoints[1], nearRoutePoints[0]) 
         
        self.playerPos[0] += self.speed * dirVector[0]
        self.playerPos[1] += self.speed * dirVector[1]
        # draw  

    def GetPlayerPos(self):
        return self.playerPos