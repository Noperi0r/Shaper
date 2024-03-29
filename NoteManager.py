import pygame
from Shape import Shaper
from Note import Note
import random

class NoteManager():
    def __init__(self):
        self.patternList = []
        self.noteLists = [] # 레벨에 있는 노트 모두 저장   
        self.stage = 0 # 0은 메인화면, 스테이지 선택. 
        self.spawnTimer = 0
     
    def GetNoteLists(self):
        return self.noteLists
     
    def LoadNotes(self, note: Note): # 노트 객체 생성 시 실행 
        self.noteLists.append(note)
     
    def LoadManager(self, stage: int): # 노트 다 불러오고, 스테이지 시작시 실행
        self.stage = stage
        self.patternList = []
        for note in self.noteLists:
            note.areaNum = -1
            note.NoteStandby()
            note.GetStageNum(stage)
            
    def SetNotesVelocity(self, speed):
        for note in self.noteLists:
            note.noteSpeed = speed
        
    def LoadPatternList(self): # 패턴 파일 읽어서 리스트에 저장. 
        if self.stage == 0:
            return
        patternFile = "./Patterns/"
        patternRange = 0
        if self.stage == 1:
            patternFile += "S1_"
            patternRange = 3 # 패턴 랜덤 숫자 넣을거
        elif self.stage == 2:
            patternFile += "S2_"
            patternRange = 4
        elif self.stage == 3:
            patternFile += "S3_"
            patternRange = 3
        
        # random pattern number set 
        #patternNum = random.randrange(patternRange)
        patternNum = random.randrange(1,patternRange+1)
        patternFile += str(patternNum)
        print(patternFile)
        
        with open(patternFile, 'r') as file: # 제목 형식 아직 안 정함
            for line in file:
                numbers = line.split()
                noteSpawnInfo = [float(num) for num in numbers]
                self.patternList.append(noteSpawnInfo)
        
        
    # 실행은 어디서? 레벨에서. 
    # while 안에서 한 번 실행되면 모두 끝날때까지 대기해야 함. 
    def PatternReady(self): # 리스트 pop 하면서 노트 ReadyNote 실행
        if self.ManagerOnTask():
            return
        while len(self.patternList) != 0:
            #print(str(len(self.patternList)))
            patternInfo = self.patternList.pop(0) # 패턴정보 AREA / SPAWNTIME 불러옴.
            patternInfo = [int(patternInfo[0]), float(patternInfo[1])]
            #print(str(patternInfo))
            
            # 몇 초뒤에 나오게 할건지에 대한 코드 추가 필요
            for note in self.noteLists:
                if note.GetAreaNum() == -1:
                    # print(len(self.noteLists)) # OK 
                    # print(patternInfo[0]) # patterninfo OK
                    note.ReadyNote(patternInfo[0], patternInfo[1]) # Isnotestandby는 false. > Releasenote 언제하지?
                    break 
        if len(self.patternList) == 0:
            self.LoadPatternList()
                
    def DeployPattern(self, borderCoords, screen, deltaTime, player):
        for note in self.noteLists:
            note.DeployNote(borderCoords, screen, deltaTime, player)
        
    def ManagerOnTask(self):
        for note in self.noteLists:
            if note.GetAreaNum() != -1:
                return True
        return False
             
 
    # def ResetManager(self) # 스테이지 종료 or 게임 오버 시 실행

    
    # 패턴 파일 기획 
    # Time, Area >> ex. 3 5 > 파일 읽어들인지 3초 뒤에 5번 영역에서 노트 생성. 
    # 속도는 동일하므로 고려 x 