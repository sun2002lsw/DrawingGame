import pygame
import drawingGame

WIDTH = 1280
HEIGHT = 720

pygame.init()
pygame.display.set_caption("이예찬 선생님의 컴퓨터 도화지")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
drawingGame.MainMenu(screen)
