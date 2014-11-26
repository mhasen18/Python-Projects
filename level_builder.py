import pygame
import time
import astar

class LevelBuilder():
	
	def __init__(self, walls, guards):
		self.walls = walls
		self.guards = guards

	def update(self):
		for guard in self.guards:
			guard.update()

	def draw(self, screen):
		gray = (51,51,51)

		for guard in self.guards:
			guard.draw(screen)
		for wall in self.walls:
			pygame.draw.rect(screen, gray, wall)
			
	def getRectGrid(self):
		"""Returns a 64x48 matrix of 0s and 1s, where 1s denote the presence of a wall"""
		
		GridList = [[0 for x in range(64)] for y in range(48)]
		for wall in self.walls:
			left_coordinate, right_coordinate = int(wall.left/16), int(wall.right/16)
			top_coordinate, bottom_coordinate = int(wall.top/16), int(wall.bottom/16)
			
			for i in range(left_coordinate, right_coordinate):
				for j in range(-2, (bottom_coordinate-top_coordinate)+2):
					if top_coordinate + j>= 0 and top_coordinate+j<=47:
						GridList[top_coordinate + j][i] = 1
				
			for i in range(top_coordinate, bottom_coordinate):
				for j in range(-2, (right_coordinate-left_coordinate)+2):
					if left_coordinate+j >= 0 and left_coordinate+j<=63:
						GridList[i][left_coordinate+j] = 1
				
		return GridList
'''
#path finding test(IGNORE)
size = (1024, 768)
rectForWalls = []
guards = []
rectForWalls = [pygame.Rect((0,352,368,32)), pygame.Rect((352,0,32,224)),
                        pygame.Rect((528,0,32,448)), pygame.Rect((702,432,336,32))]

rectForWalls.append(pygame.Rect(0,0,size[0], 32))
rectForWalls.append(pygame.Rect(0,size[1] - 32,size[0], 32))
rectForWalls.append(pygame.Rect(0, 32, 32, size[1] - 32))
rectForWalls.append(pygame.Rect(size[0] - 32, 32, 32, size[1] - 32))

level_one = LevelBuilder(rectForWalls, guards)
grd = level_one.getRectGrid()
star = astar.AStar(grd.copy(), (4,4), (40,4))
start = (4,4)

timeStart = time.time()
for i in range(25):
	if not star.notFound:
		break
	path = star.pathFind(.01)
print(time.time() - timeStart)
'''
