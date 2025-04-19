import pygame
from tkinter import colorchooser
from tkinter import messagebox


class Sculpture:
    def __init__(self):
        self._oldMousePos = None

    def Name(self):
        return "조각하기"
    
    def ResetOldMousePos(self):
        self._oldMousePos = None

    def DrawBoard(self, screen):
        return

    def HandleMouseMove(self, screen, curMousePos, pressingPower, interfaceHeight):
        if curMousePos[1] - pressingPower < interfaceHeight:
            return  # 그림이 인터페이스 영역을 침범함

        if self._oldMousePos and pressingPower:
            pygame.draw.line(screen, "black", self._oldMousePos, curMousePos, pressingPower)
        self._oldMousePos = curMousePos

    def HandleMouseWheel(self, screen, button):
        return

    def DecorateSurfaceToPrint(self, surface):
        printColor = colorchooser.askcolor(title="물감 색깔을 골라주세요")[0]
        if printColor is None:
            printColor = (255, 255, 255)

        # 파인 곳(검정색)은 흰색으로 바꾸고 나머지(도화지) 부분은 색칠 해주기
        width, height = surface.get_size()
        for x in range(width):
            for y in range(height):
                if surface.get_at((x, y)) == (0, 0, 0, 255):
                    surface.set_at((x, y), (255, 255, 255, 255))
                else:
                    surface.set_at((x, y), printColor)

        # 도화지에 찍는거니깐 좌우 반전이 되어야 함
        return pygame.transform.flip(surface, True, False)

    def ChangeColor(self):
        messagebox.showerror("색 고르기", "조각하기는 색을 고를 수 없습니다")
