import pygame
import sys

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

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 화면 배경 색 설정
    screen.fill(background_color)

    # 여기에 게임 객체 또는 렌더링 코드를 추가할 수 있습니다.

    # 화면 업데이트
    pygame.display.update()

# Pygame 종료
pygame.quit()
sys.exit()