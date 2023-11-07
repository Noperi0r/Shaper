import pygame
import sys
from Shape import Shaper
from Player import Player
from LevelClass import LevelManager
from NoteManager import NoteManager
from Note import Note
import time

# Pygame 초기화
pygame.init()

# Set Screen confs-------------
screen_width = 1024
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height))

center_x = screen_width // 2
center_y = screen_height // 2

pygame.display.set_caption("Shaper!") # 타이틀
background_color = (0, 0, 0) # 배경색 
#------------------------------

# Load LevelManager
level = LevelManager(screen)
level.Main_screen(center_x, center_y, screen)

# Spawn Objects---------------
shaper = Shaper([center_x, center_y]) # Shaper
shaper.MakeNPoints(screen, 2) # init points

noteManager = NoteManager() # NoteManager

for i in range(50):
    noteManager.LoadNotes(Note(shaper, screen)) # Notes
player = Player(shaper) # player 
#-----------------------------

# Screen switch Trigger
space_to_main = False
esc_to_level_selection = False

# Sound-----------------------
sound_Stage1 = pygame.mixer.Sound('./sound/music/stage1.mp3')
sound_Stage2 = pygame.mixer.Sound('./sound/music/stage2.mp3')
sound_Stage3 = pygame.mixer.Sound('./sound/music/stage3.mp3')
sound_Button = pygame.mixer.Sound('./sound/effect/menu_sound1.mp3')
sound_Gameover = pygame.mixer.Sound('./sound/effect/game_over.wav')

# 버퍼 설정(사운드 지연 방지)
#pygame.mixer.pre_init(44100,-16,2,2048)
sound_Stage1.set_volume(0.2)
sound_Stage2.set_volume(0.2)
sound_Stage3.set_volume(0.2)
sound_Button.set_volume(0.1)
sound_Gameover.set_volume(1.0)
#-----------------------------

# Timer and Frame-------------
FPS = 60
isTimerOn = False
seconds = 0
deltaTime= 1 / FPS
clock = pygame.time.Clock()
prevTime = time.time() 
#-----------------------------

def GetDeltaTime(prevTime):
    currentTime = time.time()
    #deltaTime = (currentTime - prevTime) % (1 / FPS)
    deltaTime = currentTime - prevTime
    prevTime = currentTime 
    return deltaTime

def Stage1Loop():
    screen.fill((0,0,0))
    shaper.MakeNPoints(screen, 4)
    
    borderCoords = shaper.DiscernNoteArea(screen, 900)
    noteManager.PatternReady() # 수정 필요
    noteManager.DeployPattern(borderCoords, screen, deltaTime, player)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            player.AngleMove(keys)
    player.DrawPlayer(screen)    
    
    shaper.MakeShapeLines(screen)
    
    if player.playerDead:
        PlayerDeadEvent(space_to_main, esc_to_level_selection, isTimerOn, seconds)
    

def Stage2Loop():
    screen.fill((0,255,100))
    shaper.MakeNPoints(screen, 6)
    
    borderCoords = shaper.DiscernNoteArea(screen, 900)

    noteManager.PatternReady() # 수정 필요
    noteManager.DeployPattern(borderCoords, screen, deltaTime, player.GetPlayerPos())
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            player.AngleMove(keys)
    player.DrawPlayer(screen)    
    
    shaper.MakeShapeLines(screen)
    
    if player.playerDead:
        PlayerDeadEvent(space_to_main, esc_to_level_selection, isTimerOn, seconds)


def Stage3Loop():
    screen.fill((0,255,100))
    shaper.MakeNPoints(screen, 14)
    
    borderCoords = shaper.DiscernNoteArea(screen, 900)

    noteManager.PatternReady() # 수정 필요
    noteManager.DeployPattern(borderCoords, screen, deltaTime, player.GetPlayerPos())
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            player.AngleMove(keys)
    player.DrawPlayer(screen)    
    
    shaper.MakeShapeLines(screen)
    
    if player.playerDead:
        PlayerDeadEvent(space_to_main, esc_to_level_selection, isTimerOn, seconds)
    
# def Stage4Loop():
playerHitGameOver = False
def PlayerDeadEvent(space_to_main, esc_to_level_selection, isTimerOn, seconds):
    level.Gameover_screen(center_x, center_y, screen, seconds)
    sound_Gameover.play()
    space_to_main = True
    esc_to_level_selection = True
    isTimerOn = False
    seconds = 0
    player.playerDead = False
    
    playerHitGameOver = True

# 메인 루프
running = True
while running:
    #screen.fill(background_color)
    #GetDeltaTime(prevTime)
        
    if level.isStage1:   
        Stage1Loop()
        isTimerOn = True
        # 타이머 출력
        if isTimerOn:
            #print(deltaTime)
            seconds = level.Update_timer(seconds, deltaTime)
        if seconds == deltaTime:
            sound_Stage1.play()

    elif level.isStage2: 
        Stage2Loop()
        isTimerOn = True
        # 타이머 출력
        if isTimerOn:
            seconds = level.Update_timer(seconds, deltaTime)
        if seconds == deltaTime:
            sound_Stage2.play()

    elif level.isStage3:
        Stage3Loop()
        isTimerOn = True
        # 타이머 출력
        if isTimerOn:
            seconds = level.Update_timer(seconds, deltaTime)
        if seconds == deltaTime:
            sound_Stage3.play()
            print('stage3')
    # elif level.isStage4:
    #     borderCoords =  shaper.DiscernNoteArea(screen, 300)
    #     GetDeltaTime()
    #     Stage4Loop()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # 메인화면
            if event.key == pygame.K_ESCAPE and space_to_main == True and esc_to_level_selection == False:
                level.Main_screen(center_x, center_y, screen)
                sound_Stage1.stop()
                sound_Stage2.stop()
                sound_Stage3.stop()
                space_to_main = False
                
            # 메인 > 레벨 전환 조건문
            if event.key == pygame.K_SPACE and space_to_main == False:
                #player.playerDead = False
                level.Level_selection(screen)
                sound_Button.play()
                space_to_main = True
                esc_to_level_selection = False
        
            # 게임 오버
            if event.key == pygame.K_ESCAPE and space_to_main == True and esc_to_level_selection == True:
                if not playerHitGameOver:
                    screen.fill((0,0,0))
                    level.Gameover_screen(center_x, center_y, screen, seconds)
                    sound_Gameover.play()
                    space_to_main = True
                    esc_to_level_selection = False
                    isTimerOn = False
                    seconds = 0
                    player.playerDead = False
                    print(playerHitGameOver)
                else:
                    playerHitGameOver = False
                    
            if space_to_main == True and esc_to_level_selection == False:
                # 레벨 1 ~ 4로 전환
                if event.key == pygame.K_1 : # 스테이지 1
                    sound_Button.play()
                    level.Level_change(1, screen)
                    space_to_main = True
                    esc_to_level_selection = True
                    isTimerOn = True
                    
                    player.LoadPlayer()
                    noteManager.LoadManager(1)
                    noteManager.LoadPatternList()

                elif event.key == pygame.K_2: # 스테이지 2
                    level.Level_change(2, screen)
                    space_to_main = True
                    esc_to_level_selection = True
                    isTimerOn = True
                    
                    player.LoadPlayer()
                    noteManager.LoadManager(2)
                    noteManager.LoadPatternList()
                    
                elif event.key == pygame.K_3: # 스테이지 3 
                    level.Level_change(3, screen) 
                    space_to_main = True
                    esc_to_level_selection = True
                    isTimerOn = True  
                    
                    player.LoadPlayer()
                    noteManager.LoadManager(3)   
                    noteManager.LoadPatternList()
                # elif event.key == pygame.K_4:
                #     level.Level_change(4, screen)
                #     space_to_main = True
                #     esc_to_level_selection = True
                #     isTimerOn = True

    pygame.display.update()
    clock.tick(FPS)

# Pygame exit
pygame.quit()
sys.exit()