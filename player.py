import pygame
import math

#rotate image by it's center(SQURE IMAGES ONLY)
def rot_center(image, rect, angle):
	"""rotate an image while keeping its center"""
	rot_image = pygame.transform.rotate(image, angle)
	rot_rect = rot_image.get_rect(center=rect.center)
	return rot_image,rot_rect

class Player:
	def __init__(self, pos, speed, level):
		#These two are to make it look like character is walking; there's probably a better way to do this
		self.x=0

		#init vats
		self.img = [pygame.image.load("res/player-right2.png").convert_alpha(), pygame.image.load("res/player-left2.png").convert_alpha()]
		self.imgStanding = pygame.image.load("res/player-standing2.png").convert_alpha()
		self.imgAttacking = pygame.image.load("res/player-knife2.png").convert_alpha()
		self.playerRect = self.img[0].get_rect()
		self.pos = pos
		self.playerRect = self.playerRect.move(pos[0], pos[1])
		self.speed = speed
		self.theta = 0
		self.level = level
		self.attacking = False
		self.standing = True
		self.collisionRect = pygame.Rect(self.playerRect.center[0] - 31, self.playerRect.center[1] - 31, 64, 64) 

	def draw(self, screen): 
		#rotate player image
		if self.standing and not self.attacking:
			rot_img = pygame.transform.rotate(self.imgStanding, self.theta)
			mag = 23
		elif not self.attacking:
			rot_img = pygame.transform.rotate(self.img[0], self.theta)
			mag = 23
		else:
			rot_img = pygame.transform.rotate(self.imgAttacking, self.theta)
			mag = 35

		rot_rect = rot_img.get_rect()

		rot_rect.center = (self.playerRect.center[0] - math.cos(math.radians(self.theta - 90)) * (mag), self.playerRect.center[1] + math.sin(math.radians(self.theta - 90)) * (mag))
			
		#draw image
		screen.blit(rot_img, rot_rect)
		pygame.draw.rect(screen, (255, 0 , 0), rot_rect, 3)

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

		#check what keys/buttons are pressed
		if keys["W"]:
			self.standing = False
			deltaF = 5
			self.x+=1
			if self.x == 5:
				self.img.append(self.img.pop(0))
				self.x = 0
		else:
			self.standing = True
		if keys["A"]:
			deltaS = -5
		if keys["S"]:
			deltaF = -5
		if keys["D"]:
			deltaS = 5
		if pygame.mouse.get_pressed()[0]:
			self.attacking = True
		else:
			self.attacking = False

		#move rectangle bsed on key input
		self.playerRect = self.playerRect.move(dirMovement[0] * deltaF, dirMovement[1] * deltaF)
		self.playerRect = self.playerRect.move(-dirMovement[1] * deltaS, dirMovement[0] * deltaS)

		#collision rect for player
		self.collisionRect = pygame.Rect(self.playerRect.center[0] - 31, self.playerRect.center[1] - 31, 64, 64)

		#check collision with walls
		for wall in self.level.walls:
			if self.collisionRect.colliderect(wall):
				self.playerRect = self.playerRect.move(-dirMovement[0] * deltaF, -dirMovement[1] * deltaF)
				self.playerRect = self.playerRect.move(dirMovement[1] * deltaS, -dirMovement[0] * deltaS)

		#move mouse to front of player
		pygame.mouse.set_pos(self.playerRect.center[0] + round(dirMovement[0] * 40), self.playerRect.center[1] + round(dirMovement[1] * 40))
