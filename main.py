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

for i in range(150):
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
    shaper.MakeNPoints(screen, 4)
    
    borderCoords = shaper.DiscernNoteArea(screen, 900, 1)
    
    # condition
    #noteManager.LoadPatternList()
    
    noteManager.PatternReady() # 수정 필요
    noteManager.DeployPattern(borderCoords, screen, deltaTime, player)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            player.AngleMove(keys)
    player.DrawPlayer(screen, 1)    
    
    shaper.MakeShapeLines(screen, 1)
    
    if player.playerDead:
        PlayerDeadEvent(seconds)
        print(gameoverByHit)
    

def Stage2Loop():
    shaper.MakeNPoints(screen, 5)
    
    borderCoords = shaper.DiscernNoteArea(screen, 900, 2)

    noteManager.PatternReady() # 수정 필요
    noteManager.DeployPattern(borderCoords, screen, deltaTime, player)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            player.AngleMove(keys)
    player.DrawPlayer(screen, 2)    
    
    shaper.MakeShapeLines(screen, 2)
    
    if player.playerDead:
        PlayerDeadEvent(seconds)
        print(gameoverByHit)


def Stage3Loop():
    shaper.MakeNPoints(screen, 14)
    
    borderCoords = shaper.DiscernNoteArea(screen, 900, 3)

    noteManager.PatternReady() # 수정 필요
    noteManager.DeployPattern(borderCoords, screen, deltaTime, player)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            player.AngleMove(keys)
    player.DrawPlayer(screen, 3)    
    
    shaper.MakeShapeLines(screen, 3)
    
    if player.playerDead:
        PlayerDeadEvent(seconds)
        print(gameoverByHit)
    
# def Stage4Loop():


gameoverByHit = False
def PlayerDeadEvent(seconds):
    global space_to_main, esc_to_level_selection, isTimerOn, gameoverByHit
    level.Gameover_screen(center_x, center_y, screen, seconds)
    sound_Gameover.play()
    space_to_main = True
    esc_to_level_selection = True
    isTimerOn = False
    seconds = 0
    player.playerDead = False
    
    gameoverByHit = True

# 메인 루프
running = True
while running:
    #screen.fill(background_color)
    #GetDeltaTime(prevTime)
        
    if level.isStage1:
        screen.fill((247, 227, 219))   
        
        isTimerOn = True
        # 타이머 출력
        if isTimerOn:
            seconds = level.Update_timer(seconds, deltaTime, 1)
        if seconds == deltaTime:
            sound_Stage1.play()
        Stage1Loop()

    elif level.isStage2: 
        screen.fill((227,232,234))   
        
        isTimerOn = True
        # 타이머 출력
        if isTimerOn:
            seconds = level.Update_timer(seconds, deltaTime, 2)
        if seconds == deltaTime:
            sound_Stage2.play()
        Stage2Loop()

    elif level.isStage3:
        screen.fill((246,224,181))
        isTimerOn = True
        # 타이머 출력
        if isTimerOn:
            seconds = level.Update_timer(seconds, deltaTime, 3)
        if seconds == deltaTime:
            sound_Stage3.play()
            print('stage3')
        Stage3Loop()

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
            if (event.key == pygame.K_ESCAPE and space_to_main == True and esc_to_level_selection == True) or player.playerDead:
                if not gameoverByHit:
                    screen.fill((0,0,0))
                    level.Gameover_screen(center_x, center_y, screen, seconds)
                    sound_Gameover.play()
                    space_to_main = True
                    esc_to_level_selection = False
                    isTimerOn = False
                    seconds = 0
                    player.playerDead = False
                    print("What")
                else:
                    gameoverByHit = False
                    
            if space_to_main == True and esc_to_level_selection == False:
                # 레벨 1 ~ 4로 전환
                if event.key == pygame.K_1 : # 스테이지 1
                    sound_Button.play()
                    level.Level_change(1)
                    space_to_main = True
                    esc_to_level_selection = True
                    isTimerOn = True
                    
                    player.LoadPlayer()
                    noteManager.LoadManager(1)
                    noteManager.LoadPatternList()
                    noteManager.SetNotesVelocity(5)


                elif event.key == pygame.K_2: # 스테이지 2
                    level.Level_change(2)
                    space_to_main = True
                    esc_to_level_selection = True
                    isTimerOn = True
                    
                    player.LoadPlayer()
                    noteManager.LoadManager(2)
                    noteManager.LoadPatternList()
                    noteManager.SetNotesVelocity(6)

                    
                elif event.key == pygame.K_3: # 스테이지 3 
                    level.Level_change(3) 
                    space_to_main = True
                    esc_to_level_selection = True
                    isTimerOn = True  
                    
                    player.LoadPlayer(4)
                    noteManager.LoadManager(3)   
                    noteManager.LoadPatternList()
                    noteManager.SetNotesVelocity(4)
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