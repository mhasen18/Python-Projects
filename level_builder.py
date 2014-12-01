import pygame
import time
import astar

class LevelBuilder():
	
	def __init__(self, walls, guards, player):
		self.walls = walls
		self.guards = guards
		for i in range(len(self.guards)):
			self.guards[i].level = self
			self.guards[i].initAStar()
		self.player = player
		self.player.level = self

	def update(self, keys):
		self.player.update(keys)
		for guard in self.guards:
			guard.update(self.player.playerRect)

	def draw(self, screen):
		gray = (51,51,51)
		self.player.draw(screen)
		for guard in self.guards:
			guard.draw(screen)
		for wall in self.walls:
			pygame.draw.rect(screen, gray, wall)
			
	def getRectGrid(self):
		"""Returns a 64x48 matrix of 0s and 1s, where 1s denote the presence of a wall"""
		
		GridList = [[0 for x in range(32)] for y in range(24)]
		for wall in self.walls:
			left_coordinate, right_coordinate = int(wall.left/32), int(wall.right/32)
			top_coordinate, bottom_coordinate = int(wall.top/32), int(wall.bottom/32)
			
			for i in range(left_coordinate, right_coordinate):
				for j in range(-1, (bottom_coordinate-top_coordinate)+1):
					if top_coordinate + j>= 0 and top_coordinate+j<=23:
						GridList[top_coordinate + j][i] = 1
				
			for i in range(top_coordinate, bottom_coordinate):
				for j in range(-1, (right_coordinate-left_coordinate)+1):
					if left_coordinate+j >= 0 and left_coordinate+j<=31:
						GridList[i][left_coordinate+j] = 1
				
		return GridList

#path finding test(IGNORE)
'''
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

star.startPath(start, (20,4))

timeStart = time.time()
for i in range(25):
	if not star.notFound:
		break
	path = star.pathFind(.01)


print(path)
print(time.time() - timeStart)

for ele in path:
	grd[ele[0]][ele[1]] = 5

for ele in grd:
	print(ele)
'''
