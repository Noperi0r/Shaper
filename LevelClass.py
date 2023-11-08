import pygame
from Shape import Shaper
from Player import Player
from enum import Enum
import sys


class LevelManager():

    def __init__(self, screen:pygame):
        self.screen = screen
        self.isStage1 = False
        self.isStage2 = False
        self.isStage3 = False
        self.isStage4 = False

    def Update_timer(self, seconds, deltaTime, stage: int):
        # seconds += clock.get_time() / 1000
        timerColor = [0,0,0]
        if stage == 1:
            timerColor = [193, 119, 121]
        elif stage == 2:
            timerColor = [112, 122, 126]
        elif stage == 3:
            timerColor = [170,111,115]
            
            
        
        seconds += deltaTime
        font = pygame.font.Font(None, 36)
        text = font.render(f" Score : {round(seconds, 2)}", True, timerColor)
        self.screen.blit(text, (600, 20))
        return seconds


    def Main_screen(self, center_x, center_y, screen:pygame):
        # 화면 지우기
        screen.fill((0,0,0))

        # 글꼴 및 글꼴 크기 설정
        font = pygame.font.Font(None, 72)  # 기본 글꼴, 글꼴 크기 72
        text = font.render("SHAPER", True, (255, 255, 255))  # 텍스트 렌더링

        # 텍스트 위치 설정
        text_x = center_x - (text.get_width() // 2)
        text_y = center_y - (text.get_height() // 2)
        screen.blit(text, (text_x, text_y))
        
        start_font = pygame.font.Font(None, 36)  # 다른 글꼴 및 크기 설정
        start_text = start_font.render("press [SPACE] to start", True, (255, 255, 255))
        start_x = center_x - (start_text.get_width() // 2)
        start_y = text_y + text.get_height() + 20  # "SHARPER" 텍스트 아래에 추가 간격
        screen.blit(start_text, (start_x, start_y))


    def Gameover_screen(self, center_x, center_y, screen:pygame, score):
        # 화면 지우기
        screen.fill((0,0,0))

        # 글꼴 및 글꼴 크기 설정
        font = pygame.font.Font(None, 72)  # 기본 글꼴, 글꼴 크기 72
        text = font.render("! GAME OVER !", True, (255, 255, 255))  # 텍스트 렌더링

        

        # 텍스트 위치 설정
        text_x = center_x - (text.get_width() // 2)
        text_y = center_y - (text.get_height() // 2)
        screen.blit(text, (text_x, text_y))


        start_font = pygame.font.Font(None, 36)  # 다른 글꼴 및 크기 설정
        start_text = start_font.render("Press Esc to Main Screen", True, (255, 255, 255))
        start_x = center_x - (start_text.get_width() // 2)
        start_y = text_y + text.get_height() + 20  # "SHARPER" 텍스트 아래에 추가 간격
        screen.blit(start_text, (start_x, start_y))  


        # 점수 표시
        score_font = pygame.font.Font(None, 36)  # 기본 글꼴, 글꼴 크기 72
        score_text = score_font.render(f" SCORE : {round(score, 2)}", True, (255, 255, 255))
        screen.blit(score_text, (start_x+75, start_y+100))
        
        self.isStage1 = False
        self.isStage2 = False
        self.isStage3 = False
        self.isStage4 = False
    
    def Level_selection(self, screen):
        # 화면 생성 + 이벤트 발생시 해당함수 호출
        screen.fill((0,0,0))
        pygame.display.set_caption("레벨 선택")
        

        # 폰트 및 크기 선택
        text_font = pygame.font.Font(None,72) 
        text_font1 = pygame.font.Font(None,48) 
        # 텍스트, 안티앨리어싱 적용, 글자색 지정
        text1 = text_font.render("[ Lv. 1 ]", True, (255, 255, 255))  
        text2 = text_font.render("[ Lv. 2 ]", True, (255, 255, 255))  
        text3 = text_font.render("[ Lv. 3 ]", True, (255, 255, 255))  
        text4 = text_font1.render("[ PRESS 1 ~ 3 ]", True, (255, 255, 255))  
        rect1 = text1.get_rect()
        rect2 = text2.get_rect()
        rect3 = text3.get_rect()
        rect4 = text4.get_rect()

        # 버튼 위치 조정
        rect1.topleft = (125, 325)  
        rect2.topleft = (450, 325)  
        rect3.topleft = (725, 325)  
        rect4.topleft = (420, 500)
        screen.blit(text1, rect1)
        screen.blit(text2, rect2)
        screen.blit(text3, rect3)
        screen.blit(text4, rect4)
        
        pygame.display.flip()
    

    def Level_change(self,  level):
        if level==1:
            print('level1')
            pygame.display.set_caption("Level 1")
            #screen.fill((255, 255, 255))
            self.isStage1 = True

        if level==2:
            print('level2')
            pygame.display.set_caption("Level 2")
            #screen.fill((255, 0, 0))
            self.isStage2 = True

        if level==3:
            print('level3')
            pygame.display.set_caption("Level 3")
            #screen.fill((0, 255, 0))
            self.isStage3 = True

        if level==4:
            print('level4')
            pygame.display.set_caption("Level 4")
            #screen.fill((0, 0, 255))
            self.isStage4 = True


    #     clock.tick(60)  # 초당 60프레임으로 제한