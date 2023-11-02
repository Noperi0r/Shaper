import pygame
from Shape import Shaper

class Player(): 
    # Init 순서는 Shaper가 먼저 이루어져야 함 
    def __init__(self, shaper : Shaper): 
        self.shaper = shaper # 상속 말고, 변수로 Shape 가져야 함.
        self.velocity = 10
        self.playerRadius = shaper.radius + 10
        self.playerPos = [shaper.centerPoint[0], shaper.centerPoint[1] + self.playerRadius]

    # def MakePlayerRoute(self):
    #     self.shaper.playerRoutePoint
        


    # def Move(self, keys : pygame.key): 
    #     # Precondition: 클래스 외부에서 L arrow, R arrow에 대한 입력에 대해서만 해당 함수 실행
    #     if keys == pygame.K_LEFT:
    #     else:
    
    def Spawn(self, surface : pygame.display ):
        pygame.draw.circle(surface, (255,255,255), self.playerPos, 7)