import pygame

def levelFileReader(filename):
    #variables
    levelRects=[]      #array to hold the rectangle object
    Speed=0
    Range=0
    fov=0
    paths=[]           #array to hold the paths of number of guards for the level

    #open file
    level_file = open(filename + '.txt')
    #read file
    level_str = level_file.read()
    #close file
    level_file.close()
    
    #taking the string and breaking it up at the guard into the rect info and the guard info
    level_list=level_str.split('Guard:')
    rect_list=level_list[0].split('\n')
    #breaking up the info for the separate rect if then appending new rects for each line
    for elm in rect_list:
        points = elm.split(',')
        levelRects.append(pygame.Rect(points[0],points[1],points[2],points[3]))

    #prepping the guard info
    guard_lines = level_list[1].split('\n')
    Speed = guard_lines[0] #first line
    Range = guard_lines[1] #second line
    fov = guard_lines[2] #third line
    #putting the paths into an array
    paths = guard_lines[3:]
        
    
