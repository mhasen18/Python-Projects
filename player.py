import pygame
import math

#rotate image by it's center(SQURE IMAGES ONLY)
def rot_center(image, rect, angle):
	"""rotate an image while keeping its center"""
	rot_image = pygame.transform.rotate(image, angle)
	rot_rect = rot_image.get_rect(center=rect.center)
	return rot_image,rot_rect

class Player:
	def __init__(self, img, pos, speed, level):
		self.img = pygame.image.load(img).convert_alpha()
		self.playerRect = self.img.get_rect()
		self.pos = pos
		self.playerRect = self.playerRect.move(pos[0], pos[1])
		self.speed = speed
		self.theta = 0
		self.level = level

	def draw(self, screen): 
		rot_image, self.playerRect = rot_center(self.img, self.playerRect, self.theta)
		screen.blit(rot_image, self.playerRect)

	def update(self, keys):
		deltaF = 0
		deltaS = 0

		#get distance between mouse and center of player
		mouseX, mouseY = pygame.mouse.get_pos()
		mouseXO, mouseYO = pygame.mouse.get_pos()
		mouseX, mouseY = mouseX - self.playerRect.center[0], mouseY - self.playerRect.center[1]
	
		#find angle at which mouse is with respect to player
		magMovement = ((mouseX ** 2) + (mouseY ** 2)) ** (1/2)
		if magMovement != 0:
			dirMovement = (mouseX / magMovement, mouseY / magMovement)
			theta = math.asin(mouseX / magMovement)
		if mouseY > 0 and mouseX < 0:
			theta = math.pi-theta
		if mouseY > 0 and mouseX >= 0:
			theta = math.pi - theta
		theta = -theta * 180 / math.pi
		#round to nearest degree to minimize jitterting
		self.theta = round(theta)

		#check what keys are pressed
		if keys["W"]:
			deltaF = 5
		if keys["A"]:
			deltaS = -5
		if keys["S"]:
			deltaF = -5
		if keys["D"]:
			deltaS = 5

		#move rectangle bsed on key input
		self.playerRect = self.playerRect.move(dirMovement[0] * deltaF, dirMovement[1] * deltaF)
		self.playerRect = self.playerRect.move(-dirMovement[1] * deltaS, dirMovement[0] * deltaS)

		collisionRect = pygame.Rect(self.playerRect.center[0] - 31, self.playerRect.center[1] - 31, 64, 64)

		for wall in self.level.walls:
			if collisionRect.colliderect(wall):
				self.playerRect = self.playerRect.move(-dirMovement[0] * deltaF, -dirMovement[1] * deltaF)
				self.playerRect = self.playerRect.move(dirMovement[1] * deltaS, -dirMovement[0] * deltaS)

		pygame.mouse.set_pos(self.playerRect.center[0] + round(dirMovement[0] * 40), self.playerRect.center[1] + round(dirMovement[1] * 40))
