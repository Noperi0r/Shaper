import pygame
from Shape import Shaper
from Note import Note

class NoteManager():
    def __init__(self, shaper: Shaper, screen: pygame.display):
        self.shaper = shaper
        self.pattern = []
        self.screen = screen
    
   
    # 이것도 player의 GetPlayerRoutePoints처럼 인덱스 작은 순대로 저장
    # areaNum은 0말고 1부터 시작해야 됨 
    def SetNoteAreas(self, areaNum): # areaNum에 따라서 인접 경계 벡터 두개 return
        if areaNum > self.shaper.n: 
            print("Area Number Error")
            return -1 
        borderVectors = self.GetAreaBorderVectors()
        if areaNum == self.shaper.n:
            return [borderVectors[0], borderVectors[areaNum-1]]
        return [borderVectors[areaNum-1], borderVectors[areaNum]]
            
    def MakeNote(self, areaNum) -> list:...
        # 노트 네 점의 좌표 필요. 
    #노트의 네 가지 좌표 도출 > draw.polygon > 네 좌표 리스트 반환
    
    def MoveNote(self, note) -> None: ...
    # 노트 각각에 대해서 작동. self.noteSpeed에 따라 네 점의 좌표 변화
    # => GetAreaBorderVectors 필요
    # 예외처리 > center좌표 도달하면 네 점 각각 모두 경우 체크하고 포지션 center로 고정.
    
    def DeleteNote(self, note) -> None: ... 
    # 도형 안으로 노트 들어가면 삭제 OR 그냥 네 점 모두 center 좌표가 되면 삭제.
    
    
    # 패턴 파일 기획 
    # Time, Area >> ex. 3 5 > 파일 읽어들인지 3초 뒤에 5번 영역에서 노트 생성. 
    # 속도는 동일하므로 고려 x 