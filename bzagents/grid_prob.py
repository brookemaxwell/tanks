#!/usr/bin/python -tt

# Create Potential Field Vectors

from __future__ import division

import math
from math import sqrt,atan2,cos,sin,pi
import time
import geometry
import numpy
from geometry import sqr, get_angle, get_distance, get_center_distance, distance_to_line, sign, Point, Vector, add_vectors, distance_and_perp_angle_to_line

class GridProbability:
	"""Class to determine obstacle locations."""

	def __init__(self):
		temp_grid = [[.1 for i in range(800)] for j in range(800)]#initialize grid
		self.prob_grid = numpy.array(temp_grid)
		self.p_ot_given_st = .97;#prob true pos
		self.p_of_given_sf = .9;#prob true neg
		
		self.p_ot_given_sf = 1 - self.p_of_given_sf#false positive
		self.p_of_given_st = 1 - self.p_ot_given_st#false negative
	
	#goes through the occgrid and updates each world coordinate with new probability
	def update_probabilities(self, occ_grid, x, y):	
			
		for col in range(len(occ_grid)):
			for row in range(len(occ_grid[0])):
				_row = x+row#+400
				_col = y+col#+400
				self.update_grid(occ_grid[col][row], _row, _col)
	
	#p(ot) = p(ot | st)p(st) + p(ot | sf)p(sf)
	def get_prob_observed_true(self, p_st):
		p_o_st = self.p_ot_given_st * p_st
		p_o_sf = self.p_ot_given_sf * (1.0-p_st)
		return p_o_st + p_o_sf
	
	#p(of) = p(of | st)p(st) + p(of | sf)p(sf)
	def get_prob_observed_false(self, p_st):
		p_o_st = self.p_of_given_st * p_st
		p_o_sf = self.p_of_given_sf * (1.0-p_st)
		return p_o_st + p_o_sf
		
	def update_grid(self, observed, x, y):
		
		p_st = self.prob_grid[x,y]# current probability of occupied=true
		
		#update the grid with probability of actually being occupied, given observation
		if observed == 1.0:
			p_ot = self.get_prob_observed_true(p_st);
			p_st_given_ot = (self.p_ot_given_st * p_st)/p_ot
			self.prob_grid[x,y]= p_st_given_ot
		else:
			p_of = self.get_prob_observed_false(p_st);
			p_st_given_of = (self.p_of_given_st * (p_st))/p_of
			self.prob_grid[x,y]= p_st_given_of
		#return self.prob_grid[x,y]
		
	def getObstacles(self):
		obstacles = []
		#make me!
		return obstacles

