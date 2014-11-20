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
		gray = (104,104,104)

		for guard in self.guards:
			guard.draw(screen)
		for wall in self.walls:
			pygame.draw.rect(screen, gray, wall)
			
	def getRectGrid(self):
		"""Returns a 64x48 matrix of 0s and 1s, where 1s denote the presence of a wall"""
	
		##Works under assumption that width of walls is 32 pixels (as in, takes up
		##two spots in the 64x48 grid). I can probably change it to work for all widths,
		##but I see no need.

		##Problem(whichc I forgot to mention)
		##Because the guards have a width, pathing them close to the walls is
		##going to cause collisions. To prevent this the walls should have
		##padding
		##i.e. a 2 thick layer of ones surronding them in the grid
		##0 0 0 0 0 0 0 0 0 0 0 0 0
		##0 0 0 0 0 0 0 0 0 0 0 0 0
		##0 0 0 0 1 1 1 1 1 0 0 0 0
		##0 0 0 0 0 0 0 0 0 0 0 0 0
		##0 0 0 0 0 0 0 0 0 0 0 0 0
		##0 0 0 0 0 0 0 0 0 0 0 0 0
		##0 0 0 0 0 0 0 0 0 0 0 0 0
		##0 0 0 0 0 0 0 0 0 0 0 0 0

		## should be(* are original wall)(sorry for not mentioning this)
		##(* should still be "1", used * to show it better)

		##0 0 0 1 1 1 1 1 1 1 0 0 0
		##0 0 1 1 1 1 1 1 1 1 1 0 0
		##0 0 1 1 * * * * * 1 1 0 0
		##0 0 1 1 1 1 1 1 1 1 1 0 0
		##0 0 0 1 1 1 1 1 1 1 0 0 0
		##0 0 0 0 0 0 0 0 0 0 0 0 0
		##0 0 0 0 0 0 0 0 0 0 0 0 0
		##0 0 0 0 0 0 0 0 0 0 0 0 0

		##Should be taken care of.

		
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