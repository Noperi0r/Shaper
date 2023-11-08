import pygame
from Shape import Shaper
import math


class Player(): 
    # Init 순서는 Shaper가 먼저 이루어져야 함 
    def __init__(self, shaper: Shaper): 
        self.shaper = shaper # 상속 말고, 변수로 Shape 가져야 함.
        self.speed = 17.5
        self.playerRadius = shaper.radius + 10
        self.playerPos = [self.shaper.playerRoutePoint[1][0], self.shaper.playerRoutePoint[1][1]]
        #self.shapeLength = math.dist(shaper.points[0], shaper.points[1]) 
        self.angleSpeed = 7
        self.playerDead = False
        
        self.playerColor = [255,255,255]

    def LoadPlayer(self, angleSpeed:int = 7):
        self.angleSpeed = angleSpeed
        self.playerPos = [self.shaper.playerRoutePoint[1][0], self.shaper.playerRoutePoint[1][1]]
        self.playerDead = False

    def RemovePlayer(self):
        self.playerPos = [0,0]

    def DrawPlayer(self, surface: pygame.display, stage: int):
        if stage == 1:
            self.playerColor = [193, 119, 121]
        elif stage == 2:
            self.playerColor = [112, 122, 126]
        elif stage == 3:
            self.playerColor = [170,111,115]
        
        pygame.draw.circle(surface, self.playerColor, self.playerPos, 10)

    def GetPlayerRoutePoints(self): # !!. 비율 안 맞긴 함
        return self.shaper.playerRoutePoint
    
    def GetNearRoutePoints(self, keys): # !!. 선분에 있을 때는 일단 판정 가능. 인접 두 점 리스트 반환
        routePoints = self.GetPlayerRoutePoints()
        availablePoints = [] 
        routeLength = math.dist(routePoints[0], routePoints[1])
        for i in range(self.shaper.n):
            if  math.dist(routePoints[i], self.playerPos) <= routeLength and len(availablePoints) < 2: # !! = 고려 필요? 
                availablePoints.append(routePoints[i]) # 0부터 n-1까지 loop 순서대로 가므로, 추가되는 것은 작은 index 순.
            elif math.dist(routePoints[i], self.playerPos) > routeLength and len(availablePoints) >= 2: # 예외처리 TESTESTESTESTESTESTSET
                 if routePoints[i] in availablePoints:
                    availablePoints.remove(routePoints[i])

        
        if len(availablePoints) == 2:
            # if self.GetPlayerRoutePoints()[self.shaper.n-1] in availablePoints and self.GetPlayerRoutePoints()[0] in availablePoints : # 마지막 선분 영역에 대한 예외 처리 
            #     print(self.GetPlayerRoutePoints()[self.shaper.n-1])
            #     #availablePoints = [availablePoints[1], availablePoints[0]] 
            #     print(availablePoints) # DEBUG
            if availablePoints[0] == routePoints[0] and availablePoints[1] == routePoints[self.shaper.n-1]: # ex. 0 5 순서 저장인 경우 예외처리 by swapping
                availablePoints = [availablePoints[1], availablePoints[0]]
            return availablePoints
        
        elif len(availablePoints) == 1:
            for i in range(len(routePoints)):
                if routePoints[i] in availablePoints: 
                    idx = i
                    break     
            if keys[pygame.K_RIGHT]: # 5 >> 0 경우 예외 
                if idx == (self.shaper.n-1):
                    availablePoints.append(routePoints[0])
                    #availablePoints = [availablePoints[1], availablePoints[0]] # 0 5
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
        elif len(availablePoints) != 2: 
            print("RouteNumber Error: length = " + str(len(availablePoints)))
            return availablePoints
            
    def Move(self, keys):
        # Precondition: 클래스 외부에서 L arrow, R arrow에 대한 입력에 대해서만 해당 함수 실행         
        nearRoutePoints = self.GetNearRoutePoints(keys)
        dirVector = [0,0]
        if keys[pygame.K_RIGHT]: # clockwise             
            dirVector[0] = nearRoutePoints[1][0] - nearRoutePoints[0][0] # default: 시계방향
            dirVector[1] = nearRoutePoints[1][1] - nearRoutePoints[0][1] 
        elif keys[pygame.K_LEFT]: #K left. Counter Clockwise 
            dirVector[0] = nearRoutePoints[0][0] - nearRoutePoints[1][0] 
            dirVector[1] = nearRoutePoints[0][1] - nearRoutePoints[1][1] 

        if math.dist(nearRoutePoints[1], nearRoutePoints[0]) == 0:
            print(nearRoutePoints[1], nearRoutePoints[0])
            return    
                
        dirVector[0] /= math.dist(nearRoutePoints[1], nearRoutePoints[0]) # Normalize
        dirVector[1] /= math.dist(nearRoutePoints[1], nearRoutePoints[0]) 
        
        self.playerPos[0] += self.speed * dirVector[0]
        self.playerPos[1] += self.speed * dirVector[1]
        # draw  

    def AngleMove(self, keys):
        radAngle = math.radians(self.angleSpeed)
        curPos = pygame.math.Vector2(self.playerPos[0], self.playerPos[1])
        center = pygame.math.Vector2(self.shaper.centerPoint[0], self.shaper.centerPoint[1])
        playerVector = [self.playerPos[0]-self.shaper.centerPoint[0], self.playerPos[1]-self.shaper.centerPoint[1]]
        
        # 선형변환 이용
        if keys[pygame.K_RIGHT]: # clockwise        
            self.playerPos[0] = self.shaper.centerPoint[0] + playerVector[0] * math.cos(radAngle) - playerVector[1] * math.sin(radAngle)
            self.playerPos[1] = self.shaper.centerPoint[1] + playerVector[0] * math.sin(radAngle) + playerVector[1] * math.cos(radAngle)
            
            #newPos = curPos.rotate_rad(radAngle)
        elif keys[pygame.K_LEFT]:         
            self.playerPos[0] = self.shaper.centerPoint[0] + playerVector[0] * math.cos(-radAngle) - playerVector[1] * math.sin(-radAngle)
            self.playerPos[1] = self.shaper.centerPoint[1] + playerVector[0] * math.sin(-radAngle) + playerVector[1] * math.cos(-radAngle)
            #newPos = curPos.rotate_rad(-radAngle)           
        #self.playerPos = [newPos.x, newPos.y]                                                          
    
    def GetPlayerPos(self):
        return self.playerPos
    
    #-----Called by LevelManager-----
    #def LoadPlayer(self) # 스테이지 로드 시 실행
    #def ResetPlayer(self) # gameover or 스테이지 종료 시 실행 
        
    