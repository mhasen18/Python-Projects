import pygame
import sys
import time
import urllib
import math
import os
import urllib.request
import io
import astar
from PIL import Image

'''
MESSAGE TO TEAMMATES:
Alright so this should be enough to get us started. I got a lot
of the annoying math shit out of the way for rotation and the
implementation of new images should require minimal change
So you guys go ahead and play around with stuff and text/email
me if you have any ideas/problems/concerns or just need some debugging.
Sky's the limit
		- JOHN
'''

'''
PROBLEMS:
-- Flashlight flickering ! FIXED !
-- 
'''

'''
TODO:
-- Walls
-- Guard vision collision detection
-- Player collision and response
-- Path finding implementation
-- Graphics
-- Level reader
-- Guard killing
-- Guard vision response(bodies)
-- etc
'''
size = (1024, 768)
xCenter, yCenter= size[0] / 2, size[1] / 2

#initialize window
screen = pygame.display.set_mode(size)

FRAMES_PER_SECOND = 30
TIME_PER_FRAME = 1.0 / 30.0
time_start = 0
timeS = time.time()
playing = True
#bools for keys
keyPressedW = False
keyPressedA = False
keyPressedS = False
keyPressedD = False

guards = []

def draw(walls):
	for wall in walls:
		pygame.draw.rect(screen,(104,104,104),wall)

pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

fileExists = os.path.isfile("player.png")
if not fileExists:
	URL = "http://i.imgur.com/14GOa9C.png"
	urllib.request.urlretrieve(URL, "player.png")

fileExists = os.path.isfile("flashlight.png")
if not fileExists:
	URL = "http://i.imgur.com/M9LEv1q.png"
	urllib.request.urlretrieve(URL, "flashlight.png")

#load image
playerImg = pygame.image.load("player.png")
flashlight = pygame.image.load("flashlight.png")

#move image to center of screen
playerRect= playerImg.get_rect().move(320, 240)

#set mouse coord right above image
pygame.mouse.set_pos(playerRect.center[0], playerRect.center[1] - 40)

#rotate image by it's center(SQURE IMAGES ONLY)
def rot_center(image, rect, angle):
	"""rotate an image while keeping its center"""
	rot_image = pygame.transform.rotate(image, angle)
	rot_rect = rot_image.get_rect(center=rect.center)
	return rot_image,rot_rect


class Guard:
	def __init__(self, imageFile, pos_, path_):
		#initialize vars
		self.path = path_
		self.speed = 4
		self.pos = [0,0]
		self.pos[0], self.pos[1] = pos_[0], pos_[1]
		self.img = pygame.image.load(imageFile)
		self.flash = pygame.image.load("flashlight.png")
		self.guardRect = self.img.get_rect()
		self.guardRect.center = self.pos
		self.startPoint = self.guardRect.center[0], self.guardRect.center[1]
		#double size of flashlight image
		self.flash = pygame.transform.scale2x(self.flash)

	def draw(self, screen):
		#rotate the image of the guard
		rot_img, self.guardRect = rot_center(self.img, self.guardRect, self.theta)

		#move pos based on speed
		self.pos[0], self.pos[1] = self.pos[0] - (self.magMove[0] * self.speed), self.pos[1] - (self.magMove[1] * self.speed)

		#move the guard based on position
		self.guardRect.center = self.pos[0], self.pos[1]

		#draw guard on screen
		screen.blit(rot_img, self.guardRect)

		#rotate flashlight
		rot_img, newRect = rot_center(self.flash, self.flash.get_rect(), self.theta)

		#position flashlight at center of guard
		newRect.center = self.guardRect.center

		#move the flashlight to tip of guard based on direction(this was hard)
		newRect.center = (newRect.center[0] + 1 - (math.sin(math.radians(self.theta)) * ( 44 + self.flash.get_height() / 2)), newRect.center[1] + 1 - (math.cos(math.radians(self.theta)) * (44 + self.flash.get_height() / 2)))

		#draw flashlight
		screen.blit(rot_img, newRect)


	def update(self):
		self.magMove = [0, 0]
		thet = 0

		#get direction of movement based on path
		dirMove = (self.startPoint[0] - self.path[0][0], self.startPoint[1] - self.path[0][1])
		
		#get unit vector for movement
		mag = ((dirMove[0] ** 2) + (dirMove[1] ** 2)) ** (1/2)

		#set the class var to the movement determine angle
		if mag != 0: 
			self.magMove[0], self.magMove[1] = dirMove[0] / mag, dirMove[1] / mag
			thet = math.asin(dirMove[0]/ mag)
		#adjust angle based of the direction of movement
		if dirMove[1] > 0 and dirMove[0] < 0:
			thet = math.pi - thet
		if dirMove[1] > 0 and dirMove[0] >= 0:
			thet = math.pi - thet
		print(self.magMove)
		#convert to degrees and assign to class var
		self.theta = (-thet * 180 / math.pi) + 180

		if math.fabs(self.path[0][0] - self.guardRect.center[0]) <= 5 and math.fabs(self.path[0][1] - self.guardRect.center[1]) <= 5:
			self.startPoint = self.path[0]
			self.guardRect.center = (self.path[0][0], self.path[0][1])
			tmp = self.path.pop(0)
			self.path.append(tmp)
		

#initialize guard
path1 =  [(80,60),(460, 60), (460,160),(80, 160)]
path2 = [(200, 600), [800, 600]]
path3 = [(60, 700), (980, 700), (980, 60), (60,60)]
path4 = [(700, 300), (900, 300), (800, 500)]

guards.append(Guard("player.png", [300,200], path1))
guards.append(Guard("player.png", [100,200], path2))
guards.append(Guard("player.png", [300,200], path3))
guards.append(Guard("player.png", [300,200], path4))

#Main Game Loop
while playing == True:
	#get the time at start of this specific cycle of loop
	time_start = time.time()

	deltaF = 0
	deltaS =0
	for ele in guards:
		ele.update()

	#check for key and mouse events
	#Polling input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
			quit
			exit
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				playing = False
			if event.key == pygame.K_w:
				keyPressedW = True
			if event.key == pygame.K_s:
				keyPressedS = True
			if event.key == pygame.K_a:
				keyPressedA = True
			if event.key == pygame.K_d:
				keyPressedD = True
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_w:
				keyPressedW = False
			if event.key == pygame.K_s:
				keyPressedS = False
			if event.key == pygame.K_a:
				keyPressedA = False
			if event.key == pygame.K_d:
				keyPressedD = False
	#get distance between mouse and center of player
	mouseX, mouseY = pygame.mouse.get_pos()
	mouseXO, mouseYO = pygame.mouse.get_pos()
	mouseX, mouseY = mouseX - playerRect.center[0], mouseY - playerRect.center[1]
	
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
	theta = round(theta)

	#check what keys are pressed
	if keyPressedW:
		deltaF = 5
	if keyPressedA:
		deltaS = -5
	if keyPressedS:
		deltaF = -5
	if keyPressedD:
		deltaS = 5



	#make screen black(erase screen)
	screen.fill((0,0,255))

	string = 'USE WASD TO MOVE AND MOUSE TO "STEER"'

	#create a new font
	pygame.font.init()
	font = pygame.font.SysFont("monospace", 18)

	#draw text on surface
	rend = font.render(string, 1, (0,0,0))

	#daw surface on screen
	screen.blit(rend, (0, 400))

	#rotate the image and its positional rectangle
	rot_image, playerRect = rot_center(playerImg, playerRect, theta)

	#move rectangle bsed on key input
	playerRect = playerRect.move(dirMovement[0] * deltaF, dirMovement[1] * deltaF)
	playerRect = playerRect.move(-dirMovement[1] * deltaS, dirMovement[0] * deltaS)

	#draw rotated img
	collisionRect = pygame.Rect(playerRect.center[0] - 32, playerRect.center[1] - 32, 64, 64)
	screen.blit(rot_image, playerRect)
	#rectForWalls = [pygame.Rect((120,180,80,100)), pygame.Rect((5,60,10,20))]
	rectForWalls = [pygame.Rect((0,350,375,25)), pygame.Rect((350,0,25,225)),
                        pygame.Rect((525,0,25,450)), pygame.Rect((700,425,324,25))]
	draw(rectForWalls)
	
	for ele in guards:
		ele.draw(screen)

	for rectangle in rectForWalls:
		if rectangle.colliderect(collisionRect):
			playerRect = playerRect.move(dirMovement[0] * -deltaF, dirMovement[1] * -deltaF)
			playerRect = playerRect.move(-dirMovement[1] * -deltaS, dirMovement[0] * -deltaS)
			

	#set mouse pos to edge of character
	pygame.mouse.set_pos(playerRect.center[0] + round(dirMovement[0] * 40), playerRect.center[1] + round(dirMovement[1] * 40))

	#update display
	pygame.display.flip()

	#sleep to maintain a constant framerate of 30 fps
	if TIME_PER_FRAME - (time.time() - time_start) > 0:
		time.sleep(TIME_PER_FRAME - (time.time() - time_start))
