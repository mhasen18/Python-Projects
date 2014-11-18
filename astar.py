import heapq

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
		self.priority = round(self.distance + self.estimate(dest) * 5)
	def __lt__(self, other):
		return self.priority < other.priority
	def estimate(self, dest):
		return (((dest[0] - self.x) ** 2) + ((dest[1] - self. y) ** 2)) ** (1 / 2)
	def __repr__(self):
		return("Node" + str(self.x) + str(self.y) + " P" + str(self.priority))

class AStar:
	def __init__(self, grid_):
		self.grid = grid_
	def pathFind(self, start, goal):
		open_nodes = []
		closed_nodes = []
		dx = [1, -1, 0, 0, 1, 1, -1, -1]
		dy = [0, 0, 1, -1, 1, -1, 1, -1]
		queue = []
		openNodes = [[0 for i in range(len(self.grid[0]))] for j in range(len(self.grid))]
		closedNodes = [[0 for i in range(len(self.grid[0]))] for j in range(len(self.grid))]

		startNode = Node(start[0], start[1], None, 0, 0)
		startNode.updatePriority(goal)
		heapq.heappush(queue, startNode)
		openNodes[startNode.x][startNode.y] = 0
		closedNodes[startNode.x][startNode.y] = 1

		while len(queue) > 0:
			curNode = heapq.heappop(queue)
			x = curNode.x
			y = curNode.y
			openNodes[x][y] = 0
			closedNodes[x][y] = 1

			if x == goal[0] and y == goal[1]:
				pathList = []
				while curNode.parent:
					pathList.append((curNode.x, curNode.y))
					curNode = curNode.parent
				return pathList[::-1]

			for i in range(len(dx)):
				childX = x + dx[i]
				childY = y + dy[i]

				if not childX < 0 and not childX > len(self.grid) - 1 and not childY < 0 and not childY > len(self.grid[0]) - 1 and self.grid[childX][childY] != 1 and closedNodes[childX][childY] != 1:
					if i < 4:
						childNode = Node(childX, childY, curNode, curNode.distance + 10, curNode.priority)
					else:
						childNode = Node(childX, childY, curNode, curNode.distance + 12, curNode.priority)
					childNode.updatePriority(goal)
					if openNodes[childX][childY] == 0:
						openNodes[childX][childY] = childNode.priority
						heapq.heappush(queue, childNode)
					elif openNodes[childX][childY] < childNode.priority:
						openNodes[childX][childY] = childNode.priority
						for i2 in range(len(queue)):
							if queue[i2].x == childX and queue[i2].y == childY:
								queue[i2] = childNode
								break
						heapq.heapify(queue)

		return None