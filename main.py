import pygame
import sys

# Pygame 초기화
pygame.init()

# 화면 크기 및 색상 정의
screen_width = 800
screen_height = 600
bg_color = (0, 0, 0)  # 검은색 배경

# Pygame 창 생성
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shaper!")

# 중심 좌표 설정
center_x = screen_width // 2
center_y = screen_height // 2

# 객체 위치 설정
object_x = 0  # 예시로 초기 객체 위치를 (0, 0)으로 설정

# 화면 정중앙 좌표 반환 함수

def Center_screen(screen_width, screen_height):

        return screen_width // 2 , screen_height // 2

# 정중앙 0,0 함수
def Center_object(object_width, object_height):
        center_object_x = center_x + object_x - object_width/2
        center_object_y = center_y - object_height/2
        return center_object_x, center_object_y

# 글꼴 및 글꼴 크기 설정
font = pygame.font.Font(None, 72)  # 기본 글꼴, 글꼴 크기 72
text = font.render("SHARPER", True, (255, 255, 255))  # 텍스트 렌더링

# 텍스트 위치 설정
text_x = center_x - (text.get_width() // 2)
text_y = center_y - (text.get_height() // 2)

# 메인 루프
running = True
show_start_text = True  # "게임 시작" 텍스트를 표시할지 여부



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                show_start_text = False  # 스페이스 바를 누르면 "게임 시작" 텍스트 숨김

    # 화면 지우기
    screen.fill(bg_color)

    # "SHARPER" 텍스트 그리기
    screen.blit(text, (text_x, text_y))

    # "게임 시작" 텍스트 그리기
    if show_start_text:
        start_font = pygame.font.Font(None, 36)  # 다른 글꼴 및 크기 설정
        start_text = start_font.render("Press SPACE to start", True, (255, 255, 255))
        start_x = center_x - (start_text.get_width() // 2)
        start_y = text_y + text.get_height() + 20  # "SHARPER" 텍스트 아래에 추가 간격
        screen.blit(start_text, (start_x, start_y))



    
    # 객체를 중심으로 그리기 (화면 중앙)
    object_width = 100  # 예시로 객체 너비 설정
    object_height = 100  # 예시로 객체 높이 설정
    object_color = (255, 0, 0)  # 예시로 객체 색상 설정
    #object_rect = pygame.Rect([center_x + object_x - object_width / 2, center_y - object_height / 2], object_width, object_height)
    print(Center_object(50,50)[0])
    
    object_rect = pygame.Rect(Center_object(object_width, object_height)[0],Center_object(object_width, object_height)[1], object_width, object_height)
    pygame.draw.rect(screen, object_color, object_rect)

    pygame.display.flip()

# Pygame 종료
pygame.quit()
sys.exit()
