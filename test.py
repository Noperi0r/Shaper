import pygame
import sys
from Shape import Shaper
from Player import Player
from Note import Note

# Pygame 초기화
pygame.init()

# 화면 크기 설정 (너비 x 높이)
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()
FPS = 60

# 화면 타이틀 설정
pygame.display.set_caption("Pygame 화면")

# 화면 색상 설정 (RGB 값)
background_color = (0, 0, 0)

hexagon = Shaper([400, 300])
hexagon.MakeNPoints(screen)

player = Player(hexagon)
noteTest = Note(hexagon, screen)  
noteTest2 = Note(hexagon, screen)  
noteTest3= Note(hexagon, screen)  

borderCoords = [] 

# 게임 루프
running = True

test = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    
            
    # 화면 배경 색 설정
    screen.fill(background_color)

    # 여기에 게임 객체 또는 렌더링 코드를 추가할 수 있습니다.
    hexagon.MakeNPoints(screen)
    hexagon.MakeShapeLines(screen)
    borderCoords = hexagon.DiscernNoteArea(screen, 300) # ★ 외부에서 실행되서 좌표 받아와야 함
    # # 경계벡터 테스트 > OK
    # for i in range(1, 7):
    #     for j in range(2):
    #         print(str(i) + " Area: "+ str(noteTest.GetAreaBorderVectors(i, borderCoords)[j]))
    
    
    # # noteTest >  GetAreaBorderVectors Test
    # test = noteTest.GetAreaBorderVectors()
    # for i in range(6):
    #     print(str(i)+ ": " + str(test[i]))
    #     pygame.draw.circle(screen ,(255,255,255),test[i], 5)
    
    # # 플레이어 이동경로 가시화 테스트 > OK
    # for i in range(0,6):
    #     if i != 0:
    #         pygame.draw.line(screen, (255, 0, 255), player.GetPlayerRoutePoints()[i],player.GetPlayerRoutePoints()[i-1], 10)
    
    if(noteTest.IsNoteStandby()):
        test = (test + 1) % 7
        print(test)
        noteTest.ReadyNote(test)
    noteTest.ReleaseNote(borderCoords, screen)
    noteTest.IsPlayerHit(player.GetPlayerPos())
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            player.Move(keys)
    player.DrawPlayer(screen)    
    
    
    # 화면 업데이트
    pygame.display.update()
    clock.tick(FPS)

# Pygame exit
pygame.quit()
sys.exit()