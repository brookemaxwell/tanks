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
		self.prob_true_pos = .97;
		self.prob_true_neg = .9;
		
	'''
	P(observed = occupied | state = occupied) is approximated as true positive rate
	P(observed = not occupied | state = occupied) is approximated as false negative rate

	P(observed = occupied | state = not occupied) is approximated as false positive rate
	P(observed = not occupied | state = not occupied) is approximated as true negative rate
	
	observed can be hit(1), miss(0), nodata(out of range...).
	'''
	def update_probabilities(self, occ_grid, x, y):	
		#print "x,y: " + str(x)+", "+ str(y)
		
		for i in range(len(occ_grid)):
			for j in range(len(occ_grid[0])):
				x = x+j
				y = y+i
				if x > 799:
					x = 799
				if y > 799:
					y = 799
				
				self.update_grid(occ_grid[i][j], x, y)
	
	def update_grid(self, observed, x, y):
		
		#get the probabilities of true/false positives/negatives
		p_ot_given_st = self.prob_true_pos
		p_ot_given_sf = 1 - self.prob_true_pos
		p_of_given_st = 1 - self.prob_true_neg
		p_of_given_sf = self.prob_true_neg
		
		
		p_st = self.prob_grid[x,y]
		
		#p(si,j = occupied | oi,j) = p(oi,j | si,j = occupied)p(si,j = occupied) / p(oi,j)
		#look into this...
		if observed == 1.0:
			p_ot = p_ot_given_st + p_ot_given_sf
			p_st_given_ot = (p_ot_given_st * p_st)/p_ot
			self.prob_grid[x,y]= p_st_given_ot
		else:
			p_of = p_of_given_st + p_of_given_sf
			p_st_given_of = (p_of_given_st * (p_st))/p_of
			self.prob_grid[x,y]= p_st_given_of
		
		return self.prob_grid[x,y]
		
	def getObstacles(self):
		obstacles = []
		#make me!
		return obstacles

