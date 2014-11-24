import heapq
import math
import time

#path finding algorithm

##TO DO: I am able to return a list of every coordinate we step though to reach
## the desired goal. If someone could write a method or something that turns that 
## into less points based on linear lines it would greatly increase performance.
## i.e Lets say points are (1,1) (1, 2) (1, 3) (1,4) (2, 5) (3, 6) (4, 7)
## could be written as (1,1) (1,4) (4, 7)
## or if points are (1,1) (1, 2) (1, 3) (1,4) (2, 7) (3, 10) (4, 13)
## could be written as (1,1) (1,4) (4, 13)

class Node:
	def __init__(self, xPos, yPos, parent, distance, priority):
		self.x = xPos
		self.y = yPos
		self.parent = parent
		self.distance = distance
		self.priority = priority
	def updatePriority(self, dest):
		#update priority of node based on heuristic
		self.priority = round(self.distance + self.estimate(dest) * 10)
	def __lt__(self, other):
		return self.priority < other.priority
	def estimate(self, dest):
		#Euclidian
		#return (((dest[0] - self.x) ** 2) + ((dest[1] - self. y) ** 2)) ** (1 / 2)
		#Manhattan
		return (math.fabs(dest[0] - self.x) + math.fabs(dest[1] - self.y))
	def __repr__(self):
		return("Node" + str(self.x) + str(self.y) + " P" + str(self.priority))

class AStar:
	def __init__(self, grid_, start, goal):
		self.grid = grid_
		self.goal = goal
		self.open_nodes = set()
		self.closed_nodes = set()
		self.queue = []
		self.openNodes = [[0 for i in range(len(self.grid[0]))] for j in range(len(self.grid))]
		self.closedNodes = [[0 for i in range(len(self.grid[0]))] for j in range(len(self.grid))]
		startNode = Node(start[0], start[1], None, 0, 0)
		startNode.updatePriority(goal)
		heapq.heappush(self.queue, startNode)
		self.openNodes[startNode.x][startNode.y] = 0
		self.closedNodes[startNode.x][startNode.y] = 1
		self.notFound = True

	def pathFind(TIME_PERMITTED):
		#send in the time we are allowing to compute this part 
		#of the path
		#(path not found at once, partitions path finding)
		dx = [1, -1, 0, 0, 1, 1, -1, -1]
		dy = [0, 0, 1, -1, 1, -1, 1, -1]
		timeStart = time.time()
		while len(self.queue) > 0 and self.notFound:

			if time.time() - timeStart > TIME_PERMITTED:
				pathList = []
				while curNode.parent:
					pathList.append((curNode.x, curNode.y))
					curNode = curNode.parent
				return pathList[::-1]

			curNode = heapq.heappop(self.queue)
			x = curNode.x
			y = curNode.y
			self.openNodes[x][y] = 0
			self.closedNodes[x][y] = 1

			if x == self.goal[0] and y == self.goal[1]:
				pathList = []
				self.notFound = False
				while curNode.parent:
					pathList.append((curNode.x, curNode.y))
					curNode = curNode.parent
				return pathList[::-1]

			for i in range(len(dx)):
				childX = x + dx[i]
				childY = y + dy[i]

				if not childX < 0 and not childX > len(self.grid) - 1 and not childY < 0 and not childY > len(self.grid[0]) - 1 and self.grid[childX][childY] != 1 and self.closedNodes[childX][childY] != 1:
					if i < 4:
						childNode = Node(childX, childY, curNode, curNode.distance + 10, curNode.priority)
					else:
						childNode = Node(childX, childY, curNode, curNode.distance + 12, curNode.priority)
					childNode.updatePriority(self.goal)
					if self.openNodes[childX][childY] == 0:
						self.openNodes[childX][childY] = childNode.priority
						heapq.heappush(self.queue, childNode)
					elif self.openNodes[childX][childY] < childNode.priority:
						self.openNodes[childX][childY] = childNode.priority
						for i2 in range(len(self.queue)):
							if self.queue[i2].x == childX and self.queue[i2].y == childY:
								self.queue[i2] = childNode
								break
						heapq.heapify(self.queue)

		return ("NOT FOUND")