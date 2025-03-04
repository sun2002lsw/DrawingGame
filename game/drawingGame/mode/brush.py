from game.etc import *
from game.ui import *


class Brush:
    def __init__(self, screen):
        self._screen = screen

        self._pressingPower = 0
        self._molarity = 100

    def Play(self):
        self._screen.fill("white")
        self._UpdateColorIndicator()
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ExitGame()
                    return

                # 마우스 휠
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  # 휠 위쪽 스크롤
                        self._molarity = max(self._molarity - 25, 0)
                        self._UpdateColorIndicator()
                    elif event.button == 5:  # 휠 아래쪽 스크롤
                        self._molarity = min(self._molarity + 25, 250)
                        self._UpdateColorIndicator()

                # 마우스 움직임
                if event.type == pygame.MOUSEMOTION:
                    self._HandleMouseMove(event.pos)

                # 키보드 누름
                if event.type == pygame.KEYDOWN:
                    if pygame.K_0 <= event.key <= pygame.K_5:
                        self._pressingPower = event.key - pygame.K_0

                    if event.key == pygame.K_ESCAPE:
                        return  # 게임 종료

    def _HandleMouseMove(self, curMousePos):
        if self._pressingPower > 0:
            pygame.draw.circle(self._screen, self._GetColorByMolarity(), curMousePos, self._pressingPower * 10)
            pygame.display.update()

    def _UpdateColorIndicator(self):
        pygame.draw.circle(self._screen, self._GetColorByMolarity(), (1250, 30), 30)
        pygame.display.update()

    def _GetColorByMolarity(self):
        return self._molarity, self._molarity, self._molarity  # 농도가 다른 먹물을 표현함
