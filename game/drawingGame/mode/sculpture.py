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
        if not self._oldMousePos or not self._pressingPower:
            self._oldMousePos = curMousePos
            return

        # 너무 미세한 움직임은 그리지 않는다
        if math.dist(self._oldMousePos, curMousePos) < 10:
            return

        # 그려진 직선에 대한 수직 선분을 구하자
        dx = curMousePos[0] - self._oldMousePos[0]
        dy = curMousePos[1] - self._oldMousePos[1]
        if dy == 0:
            dy = 0.0001
        orthogonalSlope = -dx/dy

        # 선분의 길이는 정해져 있음
        lineLength = self._pressingPower
        diff_x = lineLength / math.sqrt(1 + orthogonalSlope ** 2)
        diff_y = orthogonalSlope * diff_x

        # 해당 선분이 쭉 연결된 사각형을 그리자
        edge1 = (curMousePos[0] + diff_x, curMousePos[1] + diff_y)
        edge2 = (curMousePos[0] - diff_x, curMousePos[1] - diff_y)
        edge3 = (self._oldMousePos[0] - diff_x, self._oldMousePos[1] - diff_y)
        edge4 = (self._oldMousePos[0] + diff_x, self._oldMousePos[1] + diff_y)

        rectangle_points = [edge1, edge2, edge3, edge4]
        pygame.draw.polygon(self._screen, "black", rectangle_points)
        pygame.display.update()

        # 마우스 위치 기록
        self._oldMousePos = curMousePos

    def _Print(self, printColor):
        self._originalBoard = self._screen.copy()
        self._printed = True

        width, height = self._screen.get_size()
        for x in range(width):
            for y in range(height):
                if self._screen.get_at((x, y)) == (0, 0, 0, 255):
                    self._screen.set_at((x, y), (255, 255, 255, 255))
                else:
                    self._screen.set_at((x, y), printColor)

        pygame.display.update()

    def _RollbackPrint(self):
        self._screen.blit(self._originalBoard, (0, 0))
        self._printed = False

        pygame.display.update()
