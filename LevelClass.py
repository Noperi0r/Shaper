import pygame
from Shape import Shaper
from Player import Player
from enum import Enum
import sys



# 레벨
def Stage(Enum):
    main_screen = 1
    stage_selection = 2
    ingame = 3
    menu_screen = 4



class LevelManager():
    def __init__(self, screen:pygame):
        self.screen = screen
        
    seconds = 0
    clock = pygame.time.Clock()
   

    def Main_screen(self, center_x, center_y, screen:pygame):
        # 글꼴 및 글꼴 크기 설정
        screen.fill((0,0,0))
        font = pygame.font.Font(None, 72)  # 기본 글꼴, 글꼴 크기 72
        text = font.render("SHARPER", True, (255, 255, 255))  # 텍스트 렌더링

        # print(center_x)
        # 텍스트 위치 설정
        text_x = center_x - (text.get_width() // 2)
        text_y = center_y - (text.get_height() // 2)
        screen.blit(text, (text_x, text_y))
        
        start_font = pygame.font.Font(None, 36)  # 다른 글꼴 및 크기 설정
        start_text = start_font.render("Press SPACE to start", True, (255, 255, 255))
        start_x = center_x - (start_text.get_width() // 2)
        start_y = text_y + text.get_height() + 20  # "SHARPER" 텍스트 아래에 추가 간격
        screen.blit(start_text, (start_x, start_y))
        
    def Gameover_screen(self, center_x, center_y, screen:pygame):
        # 글꼴 및 글꼴 크기 설정
        screen.fill((0,0,0))
        font = pygame.font.Font(None, 72)  # 기본 글꼴, 글꼴 크기 72
        text = font.render("! GAME OVER !", True, (255, 255, 255))  # 텍스트 렌더링

        # 텍스트 위치 설정
        text_x = center_x - (text.get_width() // 2)
        text_y = center_y - (text.get_height() // 2)
        screen.blit(text, (text_x, text_y))


        start_font = pygame.font.Font(None, 36)  # 다른 글꼴 및 크기 설정
        start_text = start_font.render("Press SPACE to restart", True, (255, 255, 255))
        start_x = center_x - (start_text.get_width() // 2)
        start_y = text_y + text.get_height() + 20  # "SHARPER" 텍스트 아래에 추가 간격
        screen.blit(start_text, (start_x, start_y))  


    def Level_selection(self, screen):
        # 화면 생성 + 이벤트 발생시 해당함수 호출
        pygame.display.set_caption("레벨 선택")
        
        # 버튼 생성 
        text_font = pygame.font.Font(None, 36)  # 폰트 및 크기 선택
        text1 = text_font.render("[ Lv. 1 ]", True, (255, 255, 255))  # 텍스트, 안티앨리어싱 적용, 글자색 지정
        text2 = text_font.render("[ Lv. 2 ]", True, (255, 255, 255))  # 텍스트, 안티앨리어싱 적용, 글자색 지정
        text3 = text_font.render("[ Lv. 3 ]", True, (255, 255, 255))  # 텍스트, 안티앨리어싱 적용, 글자색 지정
        text4 = text_font.render("[ Lv. 4 ]", True, (255, 255, 255))  # 텍스트, 안티앨리어싱 적용, 글자색 지정
        rect1 = text1.get_rect()
        rect2 = text2.get_rect()
        rect3 = text3.get_rect()
        rect4 = text4.get_rect()

        rect1.topleft = (100, 200)  # 버튼 위치 조정
        rect2.topleft = (200, 200)  # 버튼 위치 조정
        rect3.topleft = (300, 200)  # 버튼 위치 조정
        rect4.topleft = (400, 200)  # 버튼 위치 조정
        
        screen.blit(text1, rect1)
        screen.blit(text2, rect2)
        screen.blit(text3, rect3)
        screen.blit(text4, rect4)

        pygame.display.flip()
    

    def Level_change(self,  level, screen):
        if level==1:
            screen.fill((0, 0, 0))
            self.hexagon = Shaper([400, 300])
            self.player = Player(self.hexagon)
            self.hexagon.MakeNPoints(self.screen)
            
            # 여기에 게임 객체 또는 렌더링 코드를 추가할 수 있습니다.
            self.hexagon.MakeNPoints(self.screen)
            self.hexagon.MakeShapeLines(self.screen)
            self.hexagon.DrawNoteArea(self.screen, 600)

            self.player.Spawn(self.screen)    

            keys = pygame.key.get_pressed()
            # if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            #     player.Move(keys)
        if level==2:
            print('level2')
            screen.fill((255, 0, 0))
        if level==3:
            screen.fill((0, 255, 0))
            print('level3')
        if level==4:
            screen.fill((0, 0, 255))
            print('level4')
