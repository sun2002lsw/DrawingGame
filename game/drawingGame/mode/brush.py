import pygame


class Brush:
    def __init__(self):
        width, height = pygame.display.get_surface().get_size()
        self._width = width
        self._height = height
        self._molarity = 100

    def Name(self):
        return "조각하기"

    def ResetOldMousePos(self):
        return

    def DrawBoard(self, screen):
        self._UpdateColorIndicator(screen)

    def HandleMouseMove(self, screen, curMousePos, pressingPower, interfaceHeight):
        if not pressingPower:
            return  # 펜을 띄고 있음
        if curMousePos[1] - pressingPower * 10 < interfaceHeight:
            return  # 그림이 인터페이스 영역을 침범함

        pygame.draw.circle(screen, self._GetColorByMolarity(), curMousePos, pressingPower * 10)

    def HandleMouseWheel(self, screen, button):
        if button == 4:  # 휠 위쪽 스크롤
            self._molarity = max(self._molarity - 25, 0)
            self._UpdateColorIndicator(screen)
        elif button == 5:  # 휠 아래쪽 스크롤
            self._molarity = min(self._molarity + 25, 250)
            self._UpdateColorIndicator(screen)

    def _UpdateColorIndicator(self, screen):
        center = (self._width * 29 / 30, self._height * 5 / 20)
        pygame.draw.circle(screen, self._GetColorByMolarity(), center, 30)

    def _GetColorByMolarity(self):
        return self._molarity, self._molarity, self._molarity  # 농도가 다른 먹물을 표현함
