import pygame
import sys
import time
#This is Brandon
#lets see if this works
size = (640, 480)
#initialize window
screen = pygame.display.set_mode(size)

rect = pygame.Rect(40,40,40,40)
num = 0
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

def draw(walls):
        for wall in walls:
                pygame.draw.rect(screen,(104,104,104),wall)

#Main Game Loop
while playing == True:
	#get the time at start of this specific cycle of loop
	time_start = time.time()
	deltaX = 0
	deltaY =0
	#check for key and mouse events
	#Polling input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
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

	#check what keys are pressed
	if keyPressedW:
		deltaY = -5
	if keyPressedA:
		deltaX = -5
	if keyPressedS:
		deltaY = 5
	if keyPressedD:
		deltaX = 5

	num += 1

	#make screen black(erase screen)
	screen.fill((0,0,0))

	string = "The number is" + str(num) + "THE TIME IS: " + str((time.time() - timeS) * 30)

	#create a new font
	pygame.font.init()
	font = pygame.font.SysFont("monospace", 18)

	#draw text on surface
	rend = font.render(string, 1, (255,255,255))
        
	rect = rect.move(deltaX, deltaY)
	#daw surface on screen
	screen.blit(rend, (0, 400))
	pygame.draw.rect(screen, (255,255,255), rect)
	wall_coordinates = [pygame.Rect((200,100,140,60)), pygame.Rect((12,15,89,29))]
	draw(wall_coordinates)

	#update display
	pygame.display.flip()

	#sleep to maintain a constant framerate of 30 fps
	if TIME_PER_FRAME - (time.time() - time_start) > 0:
		time.sleep(TIME_PER_FRAME - (time.time() - time_start))

time.sleep(5)
#Trying to see if this works with github
#seeing how to push to master
