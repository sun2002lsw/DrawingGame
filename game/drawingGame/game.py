from game.ui import *
from game.etc import *

from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

root = tk.Tk()
root.withdraw()


class Game:
    def __init__(self, screen, gameMode):
        self._screen = screen
        self._gameMode = gameMode
        self._pressingPower = 0

        width, height = pygame.display.get_surface().get_size()
        self._width = width
        self._height = height
        self._interfaceHeight = self._height * 2 / 10

        self._buttons = None
        self._oldScreens = list()

    def Play(self):
        self._DrawBoard()

        while True:
            # 위쪽의 인터페이스 영역 처리
            mousePos = pygame.mouse.get_pos()
            if mousePos[1] <= self._height * 2 / 10:
                cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
                pygame.mouse.set_cursor(cursor)

                for event in pygame.event.get():
                    mousePressing = pygame.mouse.get_pressed()[0]  # 왼쪽 마우스를 누르고 움직일 때
                    self._HandleInterfaceClick(mousePos, mousePressing, event.type)
                self._gameMode.ResetOldMousePos()
                continue

            # 인터페이스 버튼 클릭으로 팝업이 뜨면, 마우스 위치가 아직 호버링 위치에 있는 것으로 인식되어
            # 버튼이 계속 active 상태로 출력됨. 그냥 상시적으로 호버링 체크를 해주자
            self._HandleButtonHovering(mousePos)

            # 아래쪽의 화이트보드 영역 처리
            cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
            pygame.mouse.set_cursor(cursor)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if pygame.K_a <= event.key <= pygame.K_z:
                        curPressingPower = event.key - pygame.K_a
                        if curPressingPower == 0 and self._pressingPower > 0:
                            self._oldScreens.append(self._screen.copy())
                        self._pressingPower = curPressingPower

                if event.type == pygame.MOUSEMOTION:
                    self._gameMode.HandleMouseMove(self._screen, event.pos, self._pressingPower, self._interfaceHeight)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self._pressingPower and event.button == 1 and len(self._oldScreens) > 1:  # 왼쪽 버튼
                        self._oldScreens.pop()
                        self._screen.blit(self._oldScreens[-1], (0, 0))
                        self._gameMode.DrawBoard(self._screen)
                        pygame.display.flip()
                    if not self._pressingPower and event.button == 3:  # 오른쪽 버튼
                        if len(self._oldScreens) == 1:
                            return  # 아무것도 안 그리고 오른쪽 버튼을 누르면 종료로 인식
                        self._oldScreens = self._oldScreens[:1]
                        self._screen.blit(self._oldScreens[0], (0, 0))
                        self._gameMode.DrawBoard(self._screen)
                        pygame.display.flip()
                    if 4 <= event.button <= 5:  # 휠 돌리기
                        self._gameMode.HandleMouseWheel(self._screen, event.button)

            # 변경사항 적용
            pygame.display.flip()

    def _DrawBoard(self):
        self._screen.fill("white")
        pygame.draw.rect(self._screen, (254, 255, 194), (0, 0, self._width, self._interfaceHeight))
        self._gameMode.DrawBoard(self._screen)

        buttonY = self._interfaceHeight / 2
        button1 = Button(self._screen, self._width * 1 / 10, buttonY, "인쇄하기", self._Print)
        button2 = Button(self._screen, self._width * 3 / 10, buttonY, "저장하기", self._Save)
        button3 = Button(self._screen, self._width * 5 / 10, buttonY, "불러오기", self._Load)
        button4 = Button(self._screen, self._width * 7 / 10, buttonY, "공유하기", self._Share)
        button5 = Button(self._screen, self._width * 9 / 10, buttonY, "색 고르기", self._ChangeColor)

        self._buttons = [button1, button2, button3, button4, button5]
        self._oldScreens = [self._screen.copy()]

    def _Print(self):
        if self._pressingPower:
            self._oldScreens.append(self._screen.copy())
        self._pressingPower = 0

        # 전체 화면에서 아래쪽 화이트보드 부분만 추출
        whiteBoardRect = pygame.Rect(0, self._interfaceHeight, self._width, self._height - self._interfaceHeight)
        whiteBoardSurface = pygame.Surface(whiteBoardRect.size)
        whiteBoardSurface.blit(self._screen, (0, 0), whiteBoardRect)

        # 임시 파일에 저장해서 프린터 호출
        printSurface = self._gameMode.DecorateSurfaceToPrint(whiteBoardSurface)
        pygame.image.save(printSurface, "screenshot.png")
        os.startfile("screenshot.png", "print")

    def _Save(self):
        if self._pressingPower:
            self._oldScreens.append(self._screen.copy())
        self._pressingPower = 0

        # 전체 화면에서 아래쪽 화이트보드 부분만 추출
        whiteBoardRect = pygame.Rect(0, self._interfaceHeight, self._width, self._height - self._interfaceHeight)
        whiteBoardSurface = pygame.Surface(whiteBoardRect.size)
        whiteBoardSurface.blit(self._screen, (0, 0), whiteBoardRect)

        # 경로 폴더 없으면 만들기
        savedDir = os.path.join(os.getcwd(), "saved")
        if not os.path.exists(savedDir):
            os.makedirs(savedDir)

        targetPath = os.path.join(os.getcwd(), f"saved\\{self._gameMode.Name()}")
        if not os.path.exists(targetPath):
            os.makedirs(targetPath)

        # 현재 날짜시각을 파일 이름으로 하여 이미지 저장
        now = datetime.now()
        formatted_date = now.strftime("%m월 %d일 %H시 %M분")
        fileName = f"{self._gameMode.Name()} - {formatted_date}.png"
        filePath = os.path.join(targetPath, fileName)

        pygame.image.save(whiteBoardSurface, filePath)
        messagebox.showinfo("저장 완료", formatted_date)

    def _Load(self):
        if self._pressingPower:
            self._oldScreens.append(self._screen.copy())
        self._pressingPower = 0

        # 경로 폴더 없으면 만들기
        savedDir = os.path.join(os.getcwd(), "saved")
        if not os.path.exists(savedDir):
            os.makedirs(savedDir)

        targetPath = os.path.join(os.getcwd(), f"saved\\{self._gameMode.Name()}")
        if not os.path.exists(targetPath):
            os.makedirs(targetPath)

        # 저장된 화이트보드 찾기
        targetPath = os.path.join(os.getcwd(), f"saved\\{self._gameMode.Name()}")
        filetype = ("저장된 그림", "*.png")
        filePath = filedialog.askopenfilename(title="파일 선택", initialdir=targetPath, filetypes=[filetype])
        if filePath == "":
            return

        # 불러온 이미지를 아래쪽 화이트보드에 적용 (크기는 일치한다고 가정함)
        imageSurface = pygame.image.load(filePath)
        self._screen.blit(imageSurface, (0, self._interfaceHeight))
        self._gameMode.DrawBoard(self._screen)
        pygame.display.flip()

        self._oldScreens.append(self._screen.copy())

    def _Share(self):
        if self._pressingPower:
            self._oldScreens.append(self._screen.copy())
        self._pressingPower = 0

        messagebox.showerror("공유하기", "인터넷에 연결되지 않아 공유할 수 없습니다")

    def _ChangeColor(self):
        if self._pressingPower:
            self._oldScreens.append(self._screen.copy())
        self._pressingPower = 0

        self._gameMode.ChangeColor(self._screen)

    def _HandleInterfaceClick(self, mousePos, mousePressing, eventType):
        if eventType == pygame.QUIT:
            ExitGame()
            return

        if eventType == pygame.MOUSEBUTTONUP:
            self._HandleButtonClick(mousePos)
            return

        mousePressed = eventType == pygame.MOUSEBUTTONDOWN
        if mousePressed or mousePressing:
            self._HandleButtonPressing(mousePos)
        else:
            self._HandleButtonHovering(mousePos)

    # 마우스를 버튼 위에 올렸을 때 처리
    def _HandleButtonHovering(self, mousePos):
        for menuButton in self._buttons:
            menuButton.Hovering(mousePos)

    # 마우스를 누른채 버튼 위에 올렸을 때 처리
    def _HandleButtonPressing(self, mousePos):
        for menuButton in self._buttons:
            menuButton.Pressing(mousePos)

    # 마우스를 클릭 했을 때 처리
    def _HandleButtonClick(self, mousePos):
        for menuButton in self._buttons:
            menuButton.Click(mousePos)
