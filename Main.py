import pygame
import sys
import time

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

#Main Game Loop
while playing == True:
	#get the time at start of this specific cycle of loop
	time_start = time.time()

	#check for key and mouse events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			print("BLAHHHH")
			if event.key == pygame.K_w:
				playing = False
            
	num += 1

	#make screen black(erase screen)
	screen.fill((0,0,0))

	string = "The number is" + str(num) + "THE TIME IS: " + str((time.time() - timeS) * 30)

	#create a new font
	pygame.font.init()
	font = pygame.font.SysFont("monospace", 18)

	#draw text on surface
	rend = font.render(string, 1, (255,255,255))

	#daw surface on screen
	screen.blit(rend, (0, 400))

	#update display
	pygame.display.flip()

	#sleep to maintain a constant framerate of 30 fps
	if TIME_PER_FRAME - (time.time() - time_start) > 0:
		time.sleep(TIME_PER_FRAME - (time.time() - time_start))

time.sleep(5)
#Trying to see if this works with github
#seeing how to push to master
