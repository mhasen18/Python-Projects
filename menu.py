import pygame
import time
import sys

##Things that need fixing:
## - When Instructions or Credits is clicked, if the cursor is moved even
##   the slightest, the instruction/credit box disappears.
## - Cursor icon should change when hovering over a clickable item. Right now,
##   it's the same old arrow cursor throughout.
## - BETTER ICON DESIGNS. I just took the icons from the internet; I think we
##   should create our own, or at least choose better ones from the internet.
## - To put music or not to put music? That is the question.

##Possible Fixes:
## - Make a boolean that is toggled on when you click one of the icons
##   that will remain on until the mouse is moved outside of the icon rectangle
## - I kinda fixed your cursor thing but you need to upload a bustom cursor image
##   or use a crappy default one. There is a flickering problem which I can't figure out.
## - I think we should make our own images as well, so that the art 
## - style is the same throughout
## - We should put music, but I don't like this one.
## - Resolution independence for screen shouldn't be hard, I give an example below

pygame.init()
size = (1080, 768)
pygame.display.set_caption("Body Game")
screen = pygame.display.set_mode((1080, 768))
bgImg = pygame.image.load("res/menu-bg.jpg")

## EXAMPLE
#Example of resolution indepence, scale background img to size of screen
#When you draw your images, draw in terms of size[0] and size[1] of frame
#instead of fixed points
bgImg = pygame.transform.scale(bgImg, size)

#This is if we want to add music. I suggest we use a more fitting song/sound
#though (same thing applies for all the images I used)
pygame.mixer.music.load("res/Nas.wav")
pygame.mixer.music.play(-1)

FRAMES_PER_SECOND = 30
TIME_PER_FRAME = 1.0 / 30.0
time_start = 0
timeS = time.time()
playing = True

#Used for instructions/credit screen
def onMouseClick(JPEG):
    if event.type == pygame.MOUSEBUTTONUP:
        imgToDraw = pygame.image.load(JPEG)
        screen.blit(imgToDraw,(31,300))

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                playing = False

    screen.fill((0, 0, 0))
    screen.blit(bgImg,(0,0))
    
    playIcon = pygame.image.load("res/play.png")
    instructionsIcon = pygame.image.load("res/instructions.png")
    creditsIcon = pygame.image.load("res/credits.png")
    icon_list = [playIcon, instructionsIcon, creditsIcon]

    #Turning icon images into rects to detect when hovered over by mouse
    icon_rect_list = []
    x = 0
    for icon in icon_list:
        icon_rect = icon.get_rect()
        icon_rect.x,icon_rect.y = (160+x,200)
        icon_rect_list.append(icon_rect)

        screen.blit(icon,(160+x, 200))
        x+=100
        
    font = pygame.font.SysFont('comicsansms', 13)
    
    #Going through icons; if they are hovered over, highlight them and add
    #text underneath describing their purpose
    for i, icon in enumerate(icon_rect_list):
        if icon.collidepoint(pygame.mouse.get_pos()) and i == 0:
            playIcon = pygame.image.load("res/play_highlighted.png")
            screen.blit(playIcon, (160,200))
            playGameTxt = font.render("Play Game", 1, (255,0,0))
            screen.blit(playGameTxt, (172, 275))
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
            if event.type == pygame.MOUSEBUTTONUP:
                pygame.mixer.music.fadeout(1500)
                import Main
                sys.exit()
            break

        if icon.collidepoint(pygame.mouse.get_pos()) and i == 1:
            instructionsIcon = pygame.image.load("res/instructions_highlighted.png")
            screen.blit(instructionsIcon, (260,200))
            instructionsTxt = font.render("Instructions", 1, (255,0,0))
            screen.blit(instructionsTxt, (263, 275))
            onMouseClick("res/instructions_box.jpg")
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
            break

        if icon.collidepoint(pygame.mouse.get_pos()) and i == 2:
            creditsIcon = pygame.image.load("res/credits_highlighted.png")
            screen.blit(creditsIcon,(360,200))
            creditsTxt = font.render("Credits", 1, (255,0,0))
            screen.blit(creditsTxt, (377, 275))
            onMouseClick("res/credits_box.jpg")
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
            break

        pygame.mouse.set_cursor(*pygame.cursors.arrow)
            
    pygame.display.flip()

    #sleep to maintain a constant framerate of 30 fps
    if TIME_PER_FRAME - (time.time() - time_start) > 0:
        time.sleep(TIME_PER_FRAME - (time.time() - time_start))
