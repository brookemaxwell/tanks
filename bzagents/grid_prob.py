#!/usr/bin/python -tt

# Create Potential Field Vectors

from __future__ import division

import math
from math import sqrt,atan2,cos,sin,pi
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
			
			if p_st_given_ot > .999:
				p_st_given_ot = 1
			
			self.prob_grid[r,c]= p_st_given_ot
		else:
			p_of = self.get_prob_observed_false(p_st);
			p_st_given_of = (self.p_of_given_st * (p_st))/p_of
			if p_st_given_of < .0001:
				p_st_given_of = 0
			self.prob_grid[r,c]= p_st_given_of
		
	def getObstacles(self):
		obstacles = []
		#make me!
		return obstacles

