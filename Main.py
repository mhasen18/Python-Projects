import pygame
import sys
import time
import urllib
import math
import os
import urllib.request
import io
import astar
import player
import body
from guard import Guard
from level_builder import LevelBuilder


size = (1024, 768)
xCenter, yCenter= size[0] / 2, size[1] / 2

#initialize window
screen = pygame.display.set_mode(size)

FRAMES_PER_SECOND = 30
TIME_PER_FRAME = 1.0 / 30
time_start = 0
timeS = time.time()
playing = True
#bools for keys
keys = {"W": False, "S" : False, "D" : False, "A" : False, "SPACE" : False}

guards = []
bodies = []

pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

PLAYER_IMG = "player.png"

fileExists = os.path.isfile(PLAYER_IMG)
if not fileExists:
	URL = "http://i.imgur.com/14GOa9C.png"
	urllib.request.urlretrieve(URL, PLAYER_IMG)

rectForWalls = []
rectForWalls = [pygame.Rect((0,352,368,32)), pygame.Rect((352,0,32,224)),
                        pygame.Rect((528,0,32,448)), pygame.Rect((702,432,336,32))]

rectForWalls.append(pygame.Rect(0,0,size[0], 32))
rectForWalls.append(pygame.Rect(0,size[1] - 32,size[0], 32))
rectForWalls.append(pygame.Rect(0, 32, 32, size[1] - 32))
rectForWalls.append(pygame.Rect(size[0] - 32, 32, 32, size[1] - 32))

level_one = LevelBuilder(rectForWalls, guards)
for elem in level_one.getRectGrid():
       # print(elem)
       pass

#init player
player = player.Player(PLAYER_IMG, (612, 348), 5, level_one)

#set mouse coord right above image
pygame.mouse.set_pos(player.playerRect.center[0], player.playerRect.center[1] - 40)
        
#initialize guard
path1 =  [(300,160),(80, 160)]
path2 = [(200, 600), [800, 600]]
path3 = [(450, 100), (450, 400)]
path4 = [(700, 100), (900, 100), (900, 300), (700, 300)]

guards.append(Guard("player.png", [300,200], path1, level_one))
guards.append(Guard("player.png", [100,200], path2, level_one))
guards.append(Guard("player.png", [32,200], path3, level_one))
guards.append(Guard("player.png", [300,200], path4, level_one))
c = 50
timeSlept = 0
timePStart = time.time()
#Main Game Loop
while playing == True:
	#get the time at start of this specific cycle of loop
	time_start = time.time()

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
				keys['W'] = True
			if event.key == pygame.K_s:
				keys['S'] = True
			if event.key == pygame.K_a:
				keys['A'] = True
			if event.key == pygame.K_d:
				keys['D'] = True
			if event.key == pygame.K_SPACE:
				keys['SPACE'] = True
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_w:
				keys['W'] = False
			if event.key == pygame.K_s:
				keys['S'] = False
			if event.key == pygame.K_a:
				keys['A'] = False
			if event.key == pygame.K_d:
				keys['D'] = False
			if event.key == pygame.K_SPACE:
				keys['SPACE'] = False
	
	#check for if the player kills a guard
	for i in range(len(guards)):
		#if rects collide(will change when we have attack animation)
		if player.playerRect.colliderect(guards[i].guardRect) and player.attacking:
			#get the guard/remove it
			tmp = guards.pop(i)
			#add body in guards position
			bodies.append(body.Body(tmp.pos, tmp.theta))
			#(can only kill one guard at time[logic] so stop checking
			break

	#update everything if not paused
	if not keys['SPACE']:
		level_one.update()
		player.update(keys)
		for bodi in bodies:
			bodi.update((0, 0))

	#make screen black(erase screen)
	screen.fill((255,255,255))
	
	#draw everything
	level_one.draw(screen)
	player.draw(screen)
	for bodi in bodies:
		bodi.draw(screen)

	#update display
	pygame.display.flip()


	'''
	#print out time remaning/sec
	if time.time() - timePStart > 1:
		timePStart = time.time()
		print(timeSlept)
		timeSlept = 0
	'''
	
	#sleep to maintain a constant framerate of 30 fps
	if TIME_PER_FRAME - (time.time() - time_start) > .0002:
		timeSlept += TIME_PER_FRAME - (time.time() - time_start)
		time.sleep(TIME_PER_FRAME - (time.time() - time_start))
		



