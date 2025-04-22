from .game import *
from .mode import *


class MainMenu:
    def __init__(self, screen):
        self._screen = screen

        width, height = pygame.display.get_surface().get_size()
        self._width = width
        self._height = height

        # 마우스 커서 바꾸기 -> 메뉴 그리기 -> 메뉴 선택하기 -> 게임하기 반복
        while True:
            cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
            pygame.mouse.set_cursor(cursor)
            self._ClearScreenWithTitle()

            self._selectedMode = None
            self._SelectGameMode()

            cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_WAIT)
            pygame.mouse.set_cursor(cursor)
            ScreenBlackOut(self._screen)

            game = Game(self._screen, self._selectedMode)
            game.Play()

            cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_WAIT)
            pygame.mouse.set_cursor(cursor)
            ScreenBlackOut(self._screen)

    # 흰 바탕에 제목만 그리기
    def _ClearScreenWithTitle(self):
        self._screen.fill("white")

        # 화면 대비 적절한 크기로 타이틀 이미지 조정
        imageWidth = self._width / 2
        imageHeight = self._height / 4
        titleImg = pygame.image.load("./data/title.png")
        titleImg = pygame.transform.scale(titleImg, (imageWidth, imageHeight))

        # 타이틀 이미지를 화면 중앙부에 위치
        rect = titleImg.get_rect()
        centerX = imageWidth - (titleImg.get_width() / 2)
        centerY = imageHeight - (titleImg.get_height() / 2)
        rect = rect.move((centerX, centerY))

        self._screen.blit(titleImg, rect)
        pygame.display.flip()

    # 게임 모드 선택 과정
    def _SelectGameMode(self):
        # 버튼들 등록
        buttonX = self._width / 2
        button1 = Button(self._screen, buttonX, self._height * 10 / 20, "조각하기", self._SelectSculptureGame)
        button2 = Button(self._screen, buttonX, self._height * 13 / 20, "붓 그리기", self._SelectBrushGame)
        button3 = Button(self._screen, buttonX, self._height * 16 / 20, "나가기", ExitGame)

        self._buttons = []
        self._buttons.append(button1)
        self._buttons.append(button2)
        self._buttons.append(button3)

        # 마우스 위치 초기화
        pygame.mouse.set_pos(self._width / 2, self._height / 3)

        # 버튼을 클릭할 때까지 진행
        while True:
            mousePos = pygame.mouse.get_pos()
            mousePressing = pygame.mouse.get_pressed()[0]  # 왼쪽 마우스를 누르고 움직일 때

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ExitGame()
                    return

                if event.type == pygame.MOUSEBUTTONUP:
                    if self._HandleButtonClick(mousePos):
                        return  # 선택 과정 종료

                mousePressed = event.type == pygame.MOUSEBUTTONDOWN
                if mousePressed or mousePressing:  # 버튼을 클릭하려 하는 순간 처리
                    self._HandleButtonPressing(mousePos)
                else:  # 단순히 버튼 위를 지나가는 처리
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
            if menuButton.Click(mousePos):
                return True  # 버튼을 클릭함

        return False  # 허공을 클릭함

    # 각 게임 모드를 선택
    def _SelectSculptureGame(self):
        self._selectedMode = Sculpture()

    def _SelectBrushGame(self):
        self._selectedMode = Brush()
