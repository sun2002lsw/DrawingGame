import os
import json
import pygame

BUTTON_SIZE = 120


class Button:
    def __init__(self, screen, x, y, text, clickFunc):
        self._screen = screen
        self._x = x
        self._y = y
        self._text = text
        self._clickFunc = clickFunc

        self._SetButtonSize(BUTTON_SIZE)
        self._DrawDefaultButton()
        self._defaultState = True

        self._LoadButtonSound()
        self._alreadyHoverSound = False
        self._alreadyPressSound = False

    def _LoadButtonSound(self):
        with open("config.json") as file:
            config = json.load(file)

            hoverSoundPath = os.path.join(os.getcwd(), config["buttonHoverSound"])
            self._hoverSound = pygame.mixer.Sound(hoverSoundPath)
            self._hoverSound.set_volume(0.1)

            pressSoundPath = os.path.join(os.getcwd(), config["buttonPressSound"])
            self._pressSound = pygame.mixer.Sound(pressSoundPath)
            self._pressSound.set_volume(0.3)

            clickSoundPath = os.path.join(os.getcwd(), config["buttonClickSound"])
            self._clickSound = pygame.mixer.Sound(clickSoundPath)
            self._clickSound.set_volume(0.1)

    # 마우스를 버튼 위에 올렸을 때
    def Hovering(self, mousePos):
        if not self._CheckInsideButton(mousePos):
            return

        if not self._alreadyHoverSound:
            pygame.mixer.Sound.play(self._hoverSound)
            self._alreadyHoverSound = True

        self._DrawActiveButton(30)

    # 마우스를 누른채 버튼 위에 올렸을 때
    def Pressing(self, mousePos):
        if not self._CheckInsideButton(mousePos):
            return

        if not self._alreadyPressSound:
            pygame.mixer.Sound.play(self._pressSound)
            self._alreadyPressSound = True

        self._DrawActiveButton(25)

    # 마우스를 클릭 했을 때
    def Click(self, mousePos):
        if not self._CheckInsideButton(mousePos):
            return False

        pygame.mixer.Sound.play(self._clickSound)
        self._DrawActiveButton(35)
        self._clickFunc()
        return True

    # 마우스 위치가 버튼에 들어 있는지 확인하고, 적절하게 처리
    def _CheckInsideButton(self, mousePos):
        if not self._IsInsideButton(mousePos):
            if not self._defaultState:
                self._DrawDefaultButton()

            self._alreadyHoverSound = False
            self._alreadyPressSound = False
            return False

        return True

    # x, y 좌표가 버튼에 들어왔는지 확인
    def _IsInsideButton(self, mousePos):
        x = mousePos[0]
        y = mousePos[1]

        if x < self._buttonRect.left or self._buttonRect.right < x:
            return False
        if y < self._buttonRect.top or self._buttonRect.bottom < y:
            return False

        return True

    # 버튼 생성
    def _DrawDefaultButton(self):
        self._defaultState = True
        self._DrawButton(30, "black", "chartreuse4", False)

    def _DrawActiveButton(self, textSize):
        self._defaultState = False
        self._DrawButton(textSize, "white", "chartreuse4", True)

    def _DrawFadeoutButton(self):
        self._defaultState = False
        self._DrawButton(35, "white", (0, 0, 0), True)

    def _DrawButton(self, textSize, textColor, backgroundColor, isBold):
        font = pygame.font.SysFont("malgungothic", textSize, isBold, False)
        surface = font.render(self._text, True, textColor)
        textRect = surface.get_rect()
        textRect.center = self._buttonRect.center

        pygame.draw.rect(self._screen, backgroundColor, self._buttonRect)
        self._screen.blit(surface, textRect)

        pygame.display.update(self._buttonRect)

    def _SetButtonSize(self, buttonSize):
        left = self._x - buttonSize
        top = self._y - buttonSize / 3
        width = buttonSize * 2
        height = width / 3

        self._buttonRect = pygame.Rect(left, top, width, height)
