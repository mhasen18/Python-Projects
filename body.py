import pygame
import math

class Body:
	def __init__(self, pos, theta):
		self.pos = pos
		self.theta = -theta - 90
		self.img = pygame.transform.scale2x(pygame.image.load("res/guard-dead.png").convert_alpha())
		self.img = pygame.transform.flip(self.img, True, False)
		self.rect = self.img.get_rect()
		self.rect.center = (pos[0], pos[1])

	def draw(self, screen):
		rot_img = pygame.transform.rotate(self.img, self.theta)
		rot_rect = rot_img.get_rect()
		rot_rect.center = self.rect.center
		screen.blit(rot_img, rot_rect)

	def update(self, dirMove):
		self.pos[0], self.pos[1] = self.pos[0] + dirMove[0], self.pos[1] + dirMove[1]
		self.rect.center = (self.pos[0], self.pos[1])
