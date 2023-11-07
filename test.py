import pygame
import sys
from Shape import Shaper
from Player import Player
from Note import Note
from NoteManager import NoteManager
import time

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

nPolygonNum = 8
hexagon = Shaper([400, 300], 15)
hexagon.MakeNPoints(screen, nPolygonNum)


noteManager = NoteManager()
noteManager.LoadManager(1)

player = Player(hexagon)

for i in range(50):
    noteManager.LoadNotes(Note(hexagon, screen))
    
# noteTest = Note(hexagon, screen, noteManager)  
# noteTest2 = Note(hexagon, screen, noteManager)  
# noteTest3= Note(hexagon, screen, noteManager)  
# noteTest4= Note(hexagon, screen, noteManager)  
# noteTest5= Note(hexagon, screen, noteManager)  

noteManager.LoadPatternList()

# 게임 루프
running = True

test = 0
prevTime = time.time()

angle = 10
while running:
    currentTime = time.time()
    deltaTime = currentTime - prevTime
    prevTime = currentTime
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    
            
    # 화면 배경 색 설정
    screen.fill(background_color)

    # 여기에 게임 객체 또는 렌더링 코드를 추가할 수 있습니다.
    hexagon.MakeNPoints(screen, nPolygonNum)
    borderCoords = hexagon.DiscernNoteArea(screen, 900) # ★ 외부에서 실행되서 좌표 받아와야 함
    
    # if(noteTest.IsNoteStandby()):
    #     test = (test + 1) % 20
    #     print(test)
    #     noteTest.ReadyNote(test)
    # noteTest.ReadyNote(5)
    # noteTest2.ReadyNote(6)
    
    # noteTest.DeployNote(borderCoords, screen)
    # noteTest2.DeployNote(borderCoords, screen)
    
    # if noteTest.IsPlayerHit(player.GetPlayerPos()):
    #     print("HIT")e
    #     noteTest.NoteStandby()        
    
    noteManager.PatternReady()
    noteManager.DeployPattern(borderCoords, screen, deltaTime, player.GetPlayerPos())
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            player.Move(keys)
    player.DrawPlayer(screen)    
    
    hexagon.MakeShapeLines(screen)
    # 화면 업데이트
    pygame.display.update()
    clock.tick(FPS)

# Pygame exit
pygame.quit()
sys.exit()