import pygame
import colorsys
from tkinter import colorchooser


class Brush:
    def __init__(self):
        width, height = pygame.display.get_surface().get_size()
        self._width = width
        self._height = height
        self._brightness = 50
        self._color = (0, 0, 0)

        self._BRUSH_RATIO = 2.2

    def Name(self):
        return "붓그리기"

    def ResetOldMousePos(self):
        return

    def DrawBoard(self, screen):
        self._UpdateColorIndicator(screen)

    def HandleMouseMove(self, screen, curMousePos, pressingPower, interfaceHeight):
        if not pressingPower:
            return  # 펜을 떼고 있음

        brushSize = pressingPower * self._BRUSH_RATIO
        if curMousePos[1] - brushSize < interfaceHeight:
            return  # 그림이 인터페이스 영역을 침범함

        pygame.draw.circle(screen, self._GetColorByBrightness(), curMousePos, brushSize)

    def HandleMouseWheel(self, screen, button):
        if button == 4:  # 휠 위쪽 스크롤
            self._brightness = max(self._brightness - 5, 0)
            self._UpdateColorIndicator(screen)
        elif button == 5:  # 휠 아래쪽 스크롤
            self._brightness = min(self._brightness + 5, 100)
            self._UpdateColorIndicator(screen)

    def DecorateSurfaceToPrint(self, surface):
        center = (self._width * 29 / 30, self._height * 5 / 20)
        pygame.draw.circle(surface, "white", center, 30)
        return surface

    def ChangeColor(self, screen):
        color = colorchooser.askcolor(title="물감 색깔을 골라주세요")[0]
        if color is None:
            return

        self._brightness = 50
        self._color = color
        self._UpdateColorIndicator(screen)

    def _UpdateColorIndicator(self, screen):
        center = (self._width * 29 / 30, self._height * 5 / 20)
        pygame.draw.circle(screen, self._GetColorByBrightness(), center, 30)

    def _GetColorByBrightness(self):
        r, g, b = [c / 255.0 for c in self._color]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        r_new, g_new, b_new = colorsys.hls_to_rgb(h, self._brightness / 100, s)

        # 0~255로 되돌림
        return tuple(int(round(c * 255)) for c in (r_new, g_new, b_new))
