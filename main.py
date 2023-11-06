import pygame
import sys
from Shape import Shaper
from Player import Player
from LevelClass import LevelManager

# Pygame 초기화
pygame.init()

# 화면 크기 설정 (너비 x 높이)
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

center_x = screen_width // 2
center_y = screen_height // 2

# 화면 타이틀 설정
pygame.display.set_caption("Sharper!")

# 화면 색상 설정 (RGB 값)
background_color = (0, 0, 0)

# LevelClass Class 불러오기
level = LevelManager(screen)
level.Main_screen(center_x, center_y, screen)

# 화면 전환 트리거
space_to_main = False
esc_to_level_selection = False

# 사운드
button_sound = pygame.mixer.Sound('./sound/effect/menu_sound.mp3')


# 타이머 + 프레임 관련 설정
timer = False
seconds = 0
deltaTime=0
clock = pygame.time.Clock()
clock.tick(60)

# shaper!
shaper = Shaper([400, 300])
borderCoords =  shaper.DiscernNoteArea(screen, 300)


def Stage1Loop():
    #shaper.LoadShaper(6)
    pass
def Stage2Loop():
    pass
def Stage3Loop():
    pass
def Stage4Loop():
    pass

# 메인 루프
running = True
while running:

    # 델타 타임 관련 변수
    start_time = pygame.time.get_ticks()

    # 타이머 출력
    if timer == True :
        screen.fill((0,0,0))
        seconds = level.Update_timer(seconds, deltaTime)

    if level.isStage1 == True:   Stage1Loop()
    elif level.isStage2 == True : Stage2Loop()
    elif level.isStage3 == True : Stage3Loop()
    elif level.isStage4 == True : Stage4Loop()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:

            # 메인화면
            if(event.key == pygame.K_ESCAPE) & (space_to_main == True) & (esc_to_level_selection == False):
                level.Main_screen(center_x, center_y, screen)
                space_to_main = False
                
            # 레벨 선택
            if (event.key == pygame.K_SPACE) & (space_to_main == False):
                level.Level_selection(screen)
                space_to_main = True
                esc_to_level_selection = False
        
            # 게임 오버
            if(event.key == pygame.K_ESCAPE) & (space_to_main == True) & (esc_to_level_selection == True):
                level.Gameover_screen(center_x, center_y, screen)
                space_to_main = True
                esc_to_level_selection = False

            
            if (space_to_main == True) & (esc_to_level_selection == False):
                # 레벨 1 ~ 4로 전환
                if event.key == pygame.K_1 :
                    level.Level_change(1, screen)
                    space_to_main = True
                    esc_to_level_selection = True
                    timer = True
                elif event.key == pygame.K_2:
                    level.Level_change(2, screen)
                    space_to_main = True
                    esc_to_level_selection = True
                    timer = True
                elif event.key == pygame.K_3:
                    level.Level_change(3, screen) 
                    space_to_main = True
                    esc_to_level_selection = True
                    timer = True
                elif event.key == pygame.K_4:
                    level.Level_change(4, screen)
                    space_to_main = True
                    esc_to_level_selection = True
                    timer = True

    
    # 델타타임 관련변수
    end_time = pygame.time.get_ticks() 
    deltaTime = end_time - start_time


    pygame.display.update()

# Pygame exit
pygame.quit()
sys.exit()