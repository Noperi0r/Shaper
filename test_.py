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

level = LevelManager(screen)
level.Main_screen(center_x, center_y, screen)

# 트리거
space_to_main = False
esc_to_level_selection = False

print(screen)
# 게임 루프
running = True
while running:
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

            # 레벨 1로 전환

            if (space_to_main == True) & (esc_to_level_selection == False):
                if (event.key == pygame.K_1) :
                    level.Level_change(1, screen)
                    space_to_main = True
                    esc_to_level_selection = True
                # 레벨 2로 전환
                elif (event.key == pygame.K_2):
                    level.Level_change(2, screen)
                    space_to_main = True
                    esc_to_level_selection = True
                # 레벨 3로 전환
                elif (event.key == pygame.K_3):
                    level.Level_change(3, screen) 
                    space_to_main = True
                    esc_to_level_selection = True
                # 레벨 4로 전환
                elif (event.key == pygame.K_4):
                    level.Level_change(4, screen)
                    space_to_main = True
                    esc_to_level_selection = True

    # 화면 배경 색 설정
    #screen.fill(background_color)

    # Enum에서 1일때 2일때 3일때 작동하는 UI 조건문 만들기
    # main -> stage select -> ingame ->  
    # 화면 업데이트
    #lvm.Main_screen(center_x, center_y, screen, show_start_text=True)
    
    pygame.display.update()

# Pygame exit
pygame.quit()
sys.exit()