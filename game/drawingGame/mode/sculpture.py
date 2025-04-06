import pygame
from tkinter import messagebox
from tkinter import colorchooser


class Sculpture:
    def __init__(self):
        self._oldMousePos = None

    def Name(self):
        return "붓그리기"
    
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
