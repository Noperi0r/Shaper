import pygame
import sys
from Shape import Shaper
from Player import Player



# Pygame 초기화
pygame.init()

# 화면 크기 설정 (너비 x 높이)
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Pygame 화면")

# 화면 색상 설정 (RGB 값)
background_color = (0, 0, 0)

hexagon = Shaper([400, 300])
hexagon.MakeNPoints(screen)

player = Player(hexagon)



# 게임 루프
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 화면 배경 색 설정
    screen.fill(background_color)

    # 여기에 게임 객체 또는 렌더링 코드를 추가할 수 있습니다.
    hexagon.MakeNPoints(screen)
    hexagon.MakeShapeLines(screen)
    hexagon.DrawNoteArea(screen, 600)

    for i in range(0,6):
        if i != 0:
            pygame.draw.line(screen, (255, 0, 255), player.GetPlayerRoutePoints()[i],player.GetPlayerRoutePoints()[i-1], 10)
    player.Spawn(screen)    
    
    #---------------DEBUG FIELD------------------------- 
    #print(str(player.IsPlayerInRoute()[0])+ " / " + str(player.IsPlayerInRoute()[1]))
    print(player.GetRouteSlope())
 
    keys = pygame.key.get_pressed()
    # if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
    #     player.Move(keys)
    
    
    # 화면 업데이트
    pygame.display.update()

# Pygame exit
pygame.quit()
sys.exit()