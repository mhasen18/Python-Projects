import pygame
import sys
import time
import urllib
import math
import os
import urllib.request
import io
from PIL import Image

size = (640, 480)
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



'''
guards = []
guards.append()

class guard():
	path
	loc
	x, y
	def __init__(self):
	def update(self):
		move, do i see a body, 
		if collision:
	def draw(pygame.display):
	def getRect()



def update():
	for guard in guards:
		guard.update()
	checkColiisons()
	pass
def draw():
	for guard in guards:
		guard.draw()
	for wall in walls:
		wall.draw()

	dooors.draw()
	pass

'''
def draw(walls):
	for wall in walls:
		pygame.draw.rect(screen,(104,104,104),wall)


pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

fileExists = os.path.isfile("player.png")
if not fileExists:
	URL = "http://i.imgur.com/14GOa9C.png"
	urllib.request.urlretrieve(URL, "player.png")

#load image
playerImg = pygame.image.load("player.png")
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


#Main Game Loop
while playing == True:

	#get the time at start of this specific cycle of loop
	time_start = time.time()

	deltaF = 0
	deltaS =0

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
	screen.fill((255,255,255))

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

	#draw bounding box of img
	pygame.draw.rect(screen, (0,0,0), playerRect, 1)

	#draw rotated img
	collisionRect = pygame.Rect(playerRect.center[0] - 32, playerRect.center[1] - 32, 64, 64)
	screen.blit(rot_image, playerRect)
	rectForWalls = [pygame.Rect((120,180,80,100)), pygame.Rect((5,60,10,20))]
	draw(rectForWalls)
	
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
