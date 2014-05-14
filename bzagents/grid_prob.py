#!/usr/bin/python -tt

# Create Potential Field Vectors

from __future__ import division

import math
from math import sqrt,atan2,cos,sin,pi
import time
import geometry
from geometry import sqr, get_angle, get_distance, get_center_distance, distance_to_line, sign, Point, Vector, add_vectors, distance_and_perp_angle_to_line


class GridProbability:
	"""Class to determine obstacle locations."""

	def __init__(self, agent):
		self.agent = agent
		
	'''
	P(observed = occupied | state = occupied) is approximated as true positive rate
	P(observed = not occupied | state = occupied) is approximated as false negative rate

	P(observed = occupied | state = not occupied) is approximated as false positive rate
	P(observed = not occupied | state = not occupied) is approximated as true negative rate
	
	observed can be hit(1), miss(0), nodata(out of range...).
	'''
	def update_probability(prob_true_pos, prob_true_neg, observed, p_st):
		
		#get the probabilities of true/false positives/negatives
		p_ot_given_st = prob_true_pos
		p_ot_given_sf = 1 - prob_true_pos
		p_of_given_st = 1 - prob_true_neg
		p_of_given_sf = prob_true_neg
		
		#p(si,j = occupied | oi,j) = p(oi,j | si,j = occupied)p(si,j = occupied) / p(oi,j)
		if observed == 1:
			p_ot = p_ot_given_st + p_ot_given_sf
			p_st_given_ot = (p_ot_given_st * p_st)/p_ot
			return p_st_given_ot
		else
			p_of = p_of_given_st + p_of_given_sf
			p_sf_given_of = (p_of_given_sf * (1.0-p_st))/p_of
			return p_sf_given_of

