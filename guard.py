import pygame
import sys
import time
import urllib
import math
import os
import urllib.request
import io
import astar
import pygame.gfxdraw

def rot_center(image, rect, angle):
	"""rotate an image while keeping its center"""
	rot_image = pygame.transform.rotate(image, angle)
	rot_rect = rot_image.get_rect(center=rect.center)
	return rot_image,rot_rect

class Triangle:
	def __init__(self, pos1, pos2, pos3):
		self.pos1 = pos1
		self.pos2 = pos2
		self.pos3 = pos3

	def draw(self, screen):
		#draw triangle
		pygame.gfxdraw.filled_trigon(screen, round(self.pos1[0]), round(self.pos1[1]), round(self.pos2[0]), round(self.pos2[1]), round(self.pos3[0]), round(self.pos3[1]), (255, 255, 0,  180))


class Line:
	def __init__(self, posS,posE):
		self.startPos = posS
		self.endPos = posE
		self.distX = posE[0] - posS[0]
		self.distY = posE[1] - posS[1]
		self.mag = (self.distX ** 2 + self.distY ** 2) ** ( 1/ 2)

	def draw(self, screen, color):
		#draw line
		pygame.draw.line(screen, color, self.startPos, self.endPos)

	def nearestIntersection(self, level):
		t1, t2 = 100, 100
		#search for intersection of line and any wall
		for wall in level.walls:
			
			wallX = wall.x
			wallY = wall.y
			wallDX = wall.width
			wallDY = 0
			tmp = 0
			tmp2 = 0
			
			#top line segment of wall
			#solve two equations for two unkowns of the the two vectors(ray and wall segment)
			try:
				tmp = (self.distY * (-wallX + self.startPos[0]) + self.distX * (-self.startPos[1] + wallY)) / ((self.distY * wallDX) - (self.distX * wallDY))
				tmp2 = (wallX + wallDX * tmp - self.startPos[0]) / self.distX
			except:
				if self.distY != 0:
					tmp2 = (wallY - self.startPos[1]) / self.distY
			#find minimum step to find a wall(assuming it is on line segment[tmp being step of segment], and it is forwards)
			if tmp2 < t1 and tmp > 0 and tmp < 1 and tmp2 > 0:
				t1 = tmp2

			#left wall segment
			wallX = wall.x
			wallY = wall.y
			wallDX = 0
			wallDY = wall.height

			try:
				tmp = (self.distY * (-wallX + self.startPos[0]) + self.distX * (-self.startPos[1] + wallY)) / ((self.distY * wallDX) - (self.distX * wallDY))
				tmp2 = (wallX + wallDX * tmp - self.startPos[0]) / self.distX
			except:
				tmp = -1
			if tmp2 < t1 and tmp > 0 and tmp < 1 and tmp2 > 0:
				t1 = tmp2

			#right wall segment
			wallX = wall.x + wall.width
			wallY = wall.y + wall.height
			wallDX = 0
			wallDY = -wall.height
			
			try:
				tmp = (self.distY * (-wallX + self.startPos[0]) + self.distX * (-self.startPos[1] + wallY)) / ((self.distY * wallDX) - (self.distX * wallDY))
				tmp2 = (wallX + wallDX * tmp - self.startPos[0]) / self.distX
			except:
				tmp = -1
			if tmp2 < t1 and tmp > 0 and tmp < 1 and tmp2 > 0:
				t1 = tmp2
			
			#bottom wall segment
			wallX = wall.x + wall.width
			wallY = wall.y + wall.height
			wallDX = -wall.width
			wallDY = 0

			try:
				tmp = (self.distY * (-wallX + self.startPos[0]) + self.distX * (-self.startPos[1] + wallY)) / ((self.distY * wallDX) - (self.distX * wallDY))
				tmp2 = (wallX + wallDX * tmp - self.startPos[0]) / self.distX
			except:
				if self.distY != 0:
					tmp2 = (wallY - self.startPos[1]) / self.distY

			if tmp2 < t1 and tmp > 0 and tmp < 1 and tmp2 > 0:
				t1 = tmp2
		#get new line that ends at closest intersection point and return it
		line = Line(self.startPos, (self.startPos[0] + self.distX * t1, self.startPos[1] + self.distY * t1))
		return line

	def changeMag(self, mag):
		#change the length of a line while preserving direction
		unit = (self.distX / self.mag, self.distY / self.mag)
		self.endPos = (self.startPos[0] + unit[0] * mag, self.startPos[1] + unit[1] * mag)

	def getAngle(self, theta):
		#positive y is down
		#vector at top of circle(cartesian sin 90)
		vec = (0, -1)
		magVec = (vec[0] ** 2 + vec[1] ** 2) ** (1 / 2)
		#dot product of line and vector at top
		val = vec[0] * self.distX + vec[1] * self.distY
		#try except is for rounding errors
		try:
			#dot product rule
			ang = math.acos(val / (magVec * self.mag))
		except:
			ang = math.acos(round(val / (magVec * self.mag)))

		#if the angle is to the left it is negative(need realive angles)
		if self.distX > 0:
			return theta - ang
		else:
			return -(theta - ang)

	def __repr__(self):
		return "endPos: " + str(self.distX) + ", " + str(self.distY) + "  angle" + str(self.getAngle(math.pi))




class Guard:
	def __init__(self, pos_, path_, map_):
		#same thing as player; these two are used to make it look like they're walking
		self.x=0

		#initialize vars
		self.path = path_
		self.level = map_
		self.speed = 4
		self.range = 400
		self.fov = 60
		self.triangles = []
		self.pos = [0,0]
		self.pos[0], self.pos[1] = pos_[0], pos_[1]
		self.img = [pygame.image.load("res/guard-left.png").convert_alpha(), pygame.image.load("res/guard-right.png").convert_alpha()]
		self.guardRect = self.img[0].get_rect()
		self.guardRect.center = self.pos
		self.startPoint = self.guardRect.center[0], self.guardRect.center[1]
		self.searching = False

	def initAStar(self):
		self.star = astar.AStar(self.level.getRectGrid(), None, None)

	def draw(self, screen):
		#rotate the image of the guard
		rot_img, self.guardRect = rot_center(self.img[0], self.guardRect, self.theta)

		#draw guard on screen
		screen.blit(rot_img, self.guardRect)

		for ele in self.path:
			pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(ele[0], ele[1], 2, 2))

		points = [self.guardRect.center]
		for tri in self.triangles:
			points.append(tri.pos3)
			points.append(tri.pos1)
		pygame.gfxdraw.filled_polygon(screen, points, (255,255, 0, 128))
		#[ray.draw(screen, (0, 255, 0)) for ray in self.rays]

	def generateRays(self):
			#get the direction of movement
			dirVec = (-math.sin(math.radians(self.theta)), -math.cos(math.radians(self.theta)))
			magVec = (dirVec[0] ** 2 + dirVec[1] ** 2) ** (1 / 2)

			#trace a ray to each of the four corners of the walls
			#check to make sure that region is in your field of view
			#dot product rule to get the angle between movement and angle to corner
			#add ones that are in the field of view
			#cut off the rays at any intersection 
			for wall in self.level.walls:
				#create a line from the guard to a wall corner
				#top left corner
				line = Line(self.guardRect.center, (wall.x, wall.y))
				#get angle between that line and the line of movement(dot product rule)
				if -1 <= ((dirVec[0] * line.distX + (dirVec[1] * line.distY)) / (math.fabs(line.mag) * math.fabs(magVec))) <= 1:
					ang = math.acos((dirVec[0] * line.distX + (dirVec[1] * line.distY)) / (math.fabs(line.mag) * math.fabs(magVec)))
					ang = ang * 180 / math.pi
					ang = math.fabs(ang)
					if ang < self.fov:
						self.rays.append(line.nearestIntersection(self.level))

				#top right corner
				line = Line(self.guardRect.center, (wall.x + wall.width, wall.y))
				if -1 <= (dirVec[0] * line.distX + (dirVec[1] * line.distY)) / (math.fabs(line.mag) * math.fabs(magVec)) <= 1:
					ang = math.acos((dirVec[0] * line.distX + (dirVec[1] * line.distY)) / (math.fabs(line.mag) * math.fabs(magVec)))
					ang = ang * 180 / math.pi
					ang = math.fabs(ang)
					if ang < self.fov:
						self.rays.append(line.nearestIntersection(self.level))

				#bottom left
				line = Line(self.guardRect.center, (wall.x, wall.y + wall.height))
				if -1 <= (dirVec[0] * line.distX + (dirVec[1] * line.distY)) / (math.fabs(line.mag) * math.fabs(magVec)) <= 1:
					ang = math.acos((dirVec[0] * line.distX + (dirVec[1] * line.distY)) / (math.fabs(line.mag) * math.fabs(magVec)))
					ang = ang * 180 / math.pi
					ang = math.fabs(ang)
					if ang < self.fov:
						self.rays.append(line.nearestIntersection(self.level))
				
				#bottom right
				line = Line(self.guardRect.center, (wall.x + wall.width, wall.y + wall.height))
				if -1 <= (dirVec[0] * line.distX + (dirVec[1] * line.distY)) / (math.fabs(line.mag) * math.fabs(magVec)) <= 1:
					ang = math.acos((dirVec[0] * line.distX + (dirVec[1] * line.distY)) / (math.fabs(line.mag) * math.fabs(magVec)))
					ang = ang * 180 / math.pi
					ang = math.fabs(ang)
					if ang < self.fov:
						self.rays.append(line.nearestIntersection(self.level))
		
			#add rays at edge of field of view, and one in the center(case in which no walls are in view)
			self.rays.append(Line(self.guardRect.center, (self.guardRect.center[0] - math.sin(math.radians(self.theta + self.fov)) * self.range, self.guardRect.center[1] - math.cos(math.radians(self.theta + self.fov)) * self.range)).nearestIntersection(self.level))
			self.rays.append(Line(self.guardRect.center, (self.guardRect.center[0] - math.sin(math.radians(self.theta - self.fov)) * self.range, self.guardRect.center[1] - math.cos(math.radians(self.theta - self.fov)) * self.range)).nearestIntersection(self.level))
			#self.rays.append(Line(self.guardRect.center, (self.guardRect.center[0] - math.sin(math.radians(self.theta)) * self.range, self.guardRect.center[1] - math.cos(math.radians(self.theta)) * self.range)).nearestIntersection(self.level))

			#normalize all rays to a maximum length based on view range
			for ray in self.rays:
				if ray.mag > self.range:
					ray.changeMag(self.range)

			#sort rays based on their angle with respect to direction of motion
			self.rays = sorted(self.rays, key = lambda x: x.getAngle(math.radians(self.theta)))
		
			#create triangles formed by adjecent rays in the list
			for i in range(1, len(self.rays)):
				self.triangles.append(Triangle(self.rays[i].endPos, self.rays[i].startPos, self.rays[i - 1].endPos))

	def dot(self, v0, v1):
		return v0[0] * v1[0] + v0[1] * v1[1]

	def vecSub(self, p1, p2):
		return (p1[0] - p2[0], p1[1] - p2[1])


	def checkCollision(self, playerRect):
		point = playerRect.center
		for tri in self.triangles:
			v0 = self.vecSub(tri.pos2, tri.pos1)
			v1 = self.vecSub(tri.pos3, tri.pos1)
			v2 = self.vecSub(point, tri.pos1)

			dot00 = self.dot(v0, v0)
			dot01 = self.dot(v0, v1)
			dot02 = self.dot(v0, v2)
			dot11 = self.dot(v1, v1)
			dot12 = self.dot(v1, v2)

			if dot00 * dot11 - dot01 * dot01 != 0:
				invDenom = 1 / (dot00 * dot11 - dot01 * dot01)
				u = (dot11 * dot02 - dot01 * dot12) * invDenom
				v = (dot00 * dot12 - dot01 * dot02) * invDenom

				if u >= 0 and v >= 0 and u + v < 1:
					return True
		return False


	def update(self, playerRect):
		self.magMove = [0, 0]
		thet = 0
		self.rays = []
		self.triangles = []

		#get direction of movement based on path
		dirMove = (self.startPoint[0] - self.path[0][0], self.startPoint[1] - self.path[0][1])
		
		#get unit vector for movement
		mag = ((dirMove[0] ** 2) + (dirMove[1] ** 2)) ** (1/2)

		#set the class var to the movement determine angle
		if mag != 0: 
			self.magMove[0], self.magMove[1] = dirMove[0] / mag, dirMove[1] / mag
			thet = math.asin(dirMove[0]/ mag)
		#adjust angle based of the direction of movement
		if dirMove[1] > 0 and dirMove[0] < 0:
			thet = math.pi - thet
		if dirMove[1] > 0 and dirMove[0] >= 0:
			thet = math.pi - thet

		#convert to degrees and assign to class var
		self.theta = (-thet * 180 / math.pi) + 180

		#if guard reaches their desired path, cycle the path points
		if math.fabs(self.path[0][0] - self.guardRect.center[0]) <= 5 and math.fabs(self.path[0][1] - self.guardRect.center[1]) <= 5:
			self.startPoint = self.path[0]
			self.guardRect.center = (self.path[0][0], self.path[0][1])
			tmp = self.path.pop(0)
			if not self.searching:
				self.path.append(tmp)

		#move pos based on speed
		self.pos[0], self.pos[1] = self.pos[0] - (self.magMove[0] * self.speed), self.pos[1] - (self.magMove[1] * self.speed)


		self.x+=1
		if self.x == 10:
			self.img.append(self.img.pop(0))
			self.x = 0

		#move the guard based on position
		self.guardRect.center = self.pos[0], self.pos[1]

		#start ray-tracing vision
		self.generateRays()

		if self.searching and self.star.notFound:
				self.pathTmp = self.star.pathFind(.1)
				if not self.star.notFound:
					self.path = self.pathTmp
					self.startPoint = self.guardRect.center
					#grd = self.level.getRectGrid()

					#for ele in self.path:
					#	grd[ele[0]][ele[1]] = 5

					for i in range(len(self.path)):
						self.path[i] = self.path[i][1], self.path[i][0]

					#for ele in grd:
					#	print(ele)

					for i in range(len(self.path)):
						self.path[i] = self.path[i][0] * 32, self.path[i][1] * 32
		
		if len(self.path) <= 1:
			if len(self.path) == 0:
				self.path.append(playerRect.center)
			else:
				self.path[0] = playerRect.center
			self.startPoint = self.guardRect.center


		if self.checkCollision(playerRect) and not self.searching:
			self.searching = True
			self.star.startPath((int(self.guardRect.center[1] / 32), int(self.guardRect.center[0] / 32)), (int(playerRect.center[1] / 32), int(playerRect.center[0] / 32)))

		print(self.path)
