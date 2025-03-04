import math

from game.etc import *
from game.ui import *
from tkinter import messagebox
from tkinter import colorchooser


class Sculpture:
    def __init__(self, screen):
        self._screen = screen

        self._oldMousePos = None
        self._pressingPower = 0
        self._originalBoard = None
        self._printed = False

    def Play(self):
        self._screen.fill("white")
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ExitGame()
                    return

                # 마우스 움직임
                if event.type == pygame.MOUSEMOTION:
                    if not self._printed:
                        self._HandleMouseMove(event.pos)

                # 키보드 누름
                if event.type == pygame.KEYDOWN:
                    if pygame.K_0 <= event.key <= pygame.K_5:
                        self._pressingPower = event.key - pygame.K_0

                    if event.key == pygame.K_RETURN:
                        if not self._printed:
                            self._pressingPower = 0
                            if messagebox.askyesno("조각 끝내기", "도화지에 찍어볼까요?"):
                                paintColor = colorchooser.askcolor(title="목공판에 색칠할 물감을 골라주세요")[0]
                                self._Print(paintColor)

                    if event.key == pygame.K_ESCAPE:
                        if self._printed:
                            self._pressingPower = 0
                            if messagebox.askyesno("조각 이어하기", "조각판으로 돌아갈까요?"):
                                self._RollbackPrint()
                        else:
                            return  # 게임 종료

    def _HandleMouseMove(self, curMousePos):
        if self._oldMousePos and self._pressingPower:
            pygame.draw.line(self._screen, "black", self._oldMousePos, curMousePos, self._pressingPower)
            pygame.display.update()

        self._oldMousePos = curMousePos

    def _Print(self, printColor):
        self._originalBoard = self._screen.copy()
        self._printed = True

        # 파인 곳(검정색)은 흰색으로 바꾸고 나머지(도화지) 부분은 색칠 해주기
        width, height = self._screen.get_size()
        for x in range(width):
            for y in range(height):
                if self._screen.get_at((x, y)) == (0, 0, 0, 255):
                    self._screen.set_at((x, y), (255, 255, 255, 255))
                else:
                    self._screen.set_at((x, y), printColor)

        # 도화지에 찍는거니깐 좌우 반전이 되어야 함
        flippedBoard = pygame.transform.flip(self._screen, True, False)
        self._screen.blit(flippedBoard, (0, 0))

        pygame.display.update()

    def _RollbackPrint(self):
        self._screen.blit(self._originalBoard, (0, 0))
        self._printed = False

        pygame.display.update()
