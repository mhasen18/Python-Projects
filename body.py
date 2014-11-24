import pygame
import math

class Body:
	def __init__(self, pos, theta):
		self.pos = pos
		self.theta = theta
		self.img = pygame.image.load("dead.png").convert_alpha()
		self.rect = self.img.get_rect()
		self.rect.center = (pos[0], pos[1])

	def draw(self, screen):
		screen.blit(self.img, self.rect)

	def update(self, dirMove):
		self.pos[0], self.pos[1] = self.pos[0] + dirMove[0], self.pos[1] + dirMove[1]
		self.rect.center = (self.pos[0], self.pos[1])
