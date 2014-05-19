#!/usr/bin/python -tt

# Create Potential Field Vectors

from __future__ import division

import math
import random
from math import sqrt,atan2,cos,sin,pi
from bzrc_occ import Answer
import time
import geometry
import numpy
from geometry import sqr, get_angle, get_distance, get_center_distance, distance_to_line, sign, Point, Vector, add_vectors, distance_and_perp_angle_to_line

UNOBSERVED = .1

class GridProbability:
	"""Class to determine obstacle locations."""

	def __init__(self):
		temp_grid = [[UNOBSERVED for i in range(800)] for j in range(800)]#initialize grid
		self.prob_grid = numpy.array(temp_grid)
		self.p_ot_given_st = .97;#prob true pos
		self.p_of_given_sf = .9;#prob true neg
		
		self.p_ot_given_sf = 1 - self.p_of_given_sf#false positive
		self.p_of_given_st = 1 - self.p_ot_given_st#false negative
		self.obstacles = []
	
	'''
	goes through the occgrid and updates each world coordinate with new probability
	first convert x and y to top-left origin coordinates, then go through the occupancy grid
	and for each observation, update our world grid with an improved probability at 
	the corresponding index
	'''
	def update_probabilities(self, occ_grid, x, y):	
		#center 
		x = x + 400;
		y = y + 400;
		
		#print "x="+str(x) + ", y="+str(y)
		for i in range(len(occ_grid)):
			for j in range(len(occ_grid[0])):
				_col = x+i
				_row = y+j
				
				self.update_grid(occ_grid[i][j], _row, _col)
	
	'''
	calculates the probability of observing that the cell is occupied
	p(ot) = p(ot | st)p(st) + p(ot | sf)p(sf)
	'''
	def get_prob_observed_true(self, p_st):
		p_o_st = self.p_ot_given_st * p_st
		p_o_sf = self.p_ot_given_sf * (1.0-p_st)
		return p_o_st + p_o_sf
	
	'''
	calculates the probability of observing that the cell is not occupied
	p(of) = p(of | st)p(st) + p(of | sf)p(sf)
	'''
	def get_prob_observed_false(self, p_st):
		p_o_st = self.p_of_given_st * p_st
		p_o_sf = self.p_of_given_sf * (1.0-p_st)
		return p_o_st + p_o_sf
	
	'''
	calculates the probability that the cell is occupied given an observation of true or false.
	threshold: if the current probability > .999, assume occupied. if < .0001, assume not occupied.
	otherwise, if observed == ccupied, find P(st | ot), else find P(st | of).
	set the grid location to the resulting probability.
	'''	
	def update_grid(self, observed, r, c):
		
		p_st = self.prob_grid[r,c]# current probability of occupied=true
		
		if p_st == 1 or p_st == 0:
			return
		
		#update the grid with probability of actually being occupied, given observation
		#if observed true, find P(st | ot) else find P(st | of)
		if observed == 1.0:
			p_ot = self.get_prob_observed_true(p_st);
			p_st_given_ot = (self.p_ot_given_st * p_st)/p_ot
			
			if p_st_given_ot > .9995:
				p_st_given_ot = 1
				self.update_obstacles(r, c)
			
			self.prob_grid[r,c]= p_st_given_ot
		else:
			p_of = self.get_prob_observed_false(p_st);
			p_st_given_of = (self.p_of_given_st * (p_st))/p_of
			if p_st_given_of < .0001:
				p_st_given_of = 0
			self.prob_grid[r,c]= p_st_given_of
	
	def new_obstacle(self, row, col):
		obstacle = []
		obstacle.append((col, row))
		obstacle.append((col, row))
		obstacle.append((col, row))
		obstacle.append((col, row))
		self.obstacles.append(obstacle)
	
	def update_obstacles(self, grid_row, grid_col):
		obs = self.obstacles
		
		row = grid_row - int(len(self.prob_grid) / 2)
		col = grid_col - int(len(self.prob_grid[0]) / 2)
		
		if len(obs) == 0: 
			self.new_obstacle(row, col)
			return
		else:
			for i in range(len(obs)):
				obstacle = obs[i]
				tl = obstacle[0]
				tr = obstacle[1]
				br = obstacle[2]
				bl = obstacle[3]
				
				print obstacle
				print "row ="+str(row) + ", col="+str(col)
				
				if col >= tl[0] and col <= tr[0]: 
					if(row <= tl[1] and row >= bl[1]):
						return; #between existing
					#elif row > tl[1] + 5 or row < bl[1] - 5:
					#	self.new_obstacle(row, col)
					elif row > tl[1]:
						tl = (tl[0], row)#tl[1] = row
						tr = (tr[0], row)#tr[1] = row
					elif row < bl[1]:
						bl = (bl[0], row)#bl[1] = row
						br = (br[0], row)#br[1] = row
				#elif col > tl[0] + 5 or col < tr[0] - 5:
				#	self.new_obstacle(row, col)
				elif col > tl[0]:
					tl = (col, tl[1])#tl[0] = col
					tr = (col, tr[1])#tr[0] = col
				elif col < tr[0]:
					bl = (col, bl[1])#bl[0] = col
					br = (col, br[1])#br[0] = col
					
						
			obstacle[0] = tl	
			obstacle[1] = tr	
			obstacle[2] = br	
			obstacle[3] = bl
			self.obstacles[i] = obstacle
		
		
	
	def getObstacles(self):
		obstacles = []
		'''for x in xrange(-399, 399, 10):
			for y in xrange(-399, 399, 10):
				if 1 == self.prob_grid[x+400][y+400]:
					obstacle = Answer()
					obstacle.x = x
					obstacle.y = y
					obstacles.append(obstacle)
		'''
		'''_world_row_min = -int(len(self.prob_grid) / 2) + 1
		_world_row_max = int(len(self.prob_grid) / 2) - 1
		_world_col_min = -int(len(self.prob_grid[0]) / 2) + 1
		_world_col_max = int(len(self.prob_grid[0]) / 2) - 1
		
		rows = []
		for row in xrange(_world_row_min, _world_row_max, 1):
			col_min = _world_col_min -1
			col_max = _world_col_min -1
			for col in xrange(_world_col_min, _world_col_max, 1):
				obs = self.prob_grid[row + 400][col + 400]
				if obs == 1.0:
					if self.prob_grid[row + 400][col + 400 - 1] == 0:
						col_min = col
						col_max = col
					elif self.prob_grid[row + 400][col + 400 + 1] == 0:
						col_max = col
						rows.append((row, col_min, col_max))
						#col_min = col
						
		#print len(rows)
		if len(rows) > 0:
			print rows[0]
		'''				
			
		if len(self.obstacles) > 0:
			print "obstacle count:"+str(len(self.obstacles))
		return self.obstacles
	
	""" Method which returns the nearest unknown part of the graph. This is used as a goal
	    The returned value needs to have an x and a y value so we use the answer class"""
	def getNearestUnknownPoint(self, tank, lastTargets):
		#print "x and y is ("+ str(xOrg) +", "+str(yOrg)+ ")"
		if hasattr(lastTargets[tank.index], 'x'):
			return lastTargets[tank.index]
		
		xOrg = tank.x
		yOrg = tank.y
		answer = Answer()
		answer.x = -1
		answer.y = -1
		while answer.x == -1 and answer.y == -1:
			x = random.randint(-398, 398)
			y = random.randint(-398, 398)
			if self.unobserved(x,y):
				#switch x, y for row, col format
				answer.x = y
				answer.y = x
				break
				
		
		print "tank at ("+ str(xOrg) +", "+str(yOrg)+ ") going to ("+ str(answer.x) +", "+str(answer.y)+")"
		lastTargets[tank.index] = answer		
				
		return answer
		
	def uniqueTarget(self, tank, lastTargets,x,y):
		for i in range(len(lastTargets)):
			if i == tank.index:
				continue
			if hasattr(lastTargets[i], 'x'):
				if lastTargets[i].x == x and lastTargets[i].y == y:
					return False
		return True
	
	def unobserved(self, orgX ,orgY):
		x= orgX + 400
		y= orgY + 400
		topRow = self.prob_grid[x-1][y+1] and self.prob_grid[x][y+1] == UNOBSERVED and self.prob_grid[x+1][y+1] == UNOBSERVED 
		middleRow = self.prob_grid[x-1][y] == UNOBSERVED and self.prob_grid[x][y] == UNOBSERVED and self.prob_grid[x+1][y] == UNOBSERVED 
		bottomRow = self.prob_grid[x-1][y-1] == UNOBSERVED and self.prob_grid[x][y-1] == UNOBSERVED and self.prob_grid[x+1][y-1] == UNOBSERVED
		return topRow and middleRow and bottomRow 

