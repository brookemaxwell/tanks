#!/usr/bin/python -tt

# Create Potential Field Vectors

from __future__ import division

import math
from math import sqrt,atan2,cos,sin,pi
import time
import geometry
from geometry import sqr, get_angle, get_distance, get_center_distance, distance_to_line, sign, Point, Vector, add_vectors, distance_and_perp_angle_to_line


class PotentialField:
	"""Class to calculate a potential field vector for an agent to follow."""

	def __init__(self, agent):
		self.agent = agent
 
	""" finds the four distances from a tank to a rectangle's four corners"""
	def __get_point_distances(self, mytank, obstacle):
		d1 = get_distance(Point(obstacle[0]), mytank)
		d2 = get_distance(Point(obstacle[1]), mytank)
		d3 = get_distance(Point(obstacle[2]), mytank)
		d4 = get_distance(Point(obstacle[3]), mytank)
		
		return [d1, d2, d3, d4]
	
	""" finds the four distances from a tank to a rectangle's four sides"""
	def __get_line_distances(self, mytank, obstacle):
		
		d1, a1 = distance_and_perp_angle_to_line(mytank, Point(obstacle[0]), Point(obstacle[1]))
		d2, a2 = distance_and_perp_angle_to_line(mytank, Point(obstacle[1]), Point(obstacle[2]))
		d3, a3 = distance_and_perp_angle_to_line(mytank, Point(obstacle[2]), Point(obstacle[3]))
		d4, a4 = distance_and_perp_angle_to_line(mytank, Point(obstacle[3]), Point(obstacle[0]))
		
		return ([d1, d2, d3, d4],[a1, a2, a3, a4])

	""" gets a repulsive vector: find distance to the enemy center, calculate angle then dx, dy. return a vector using dx, dy"""
	def get_repulse_field(self, mytank, obj, r, s, b):
		
		d = get_center_distance(mytank, obj)
		theta = get_angle(mytank, obj)
		
		dx = 0
		dy = 0
		
		if d < r:
			dx = -sign(cos(theta))*float('inf')
			dy = -sign(sin(theta))*float('inf')
		elif d >= r and d <= s+r:
			dx = -b * (s + r - d) * cos(theta)
			dy = -b * (s + r - d) * sin(theta)
			
		#else dx, dy = 0
				
		vector = Vector()
		vector.set_x_and_y(dx, dy)
		
		return vector

	""" gets an attractive vector: find distance to the goal center, calculate angle then dx, dy. return a vector using dx, dy"""
	def get_attract_field(self, mytank, obj, r, s, a):
		
		d = get_center_distance(mytank, obj)
		theta = get_angle(mytank, obj)
		
		dx = 0;
		dy = 0
		
		if d > (s+r):
			dx = a * s * cos(theta)
			dy = a * s * sin(theta)
		elif d >= r: #and d<=s+r
			dx = a * (d-r) * cos(theta)
			dy = a * (d-r) * sin(theta)
		#else dx = 0 dy = 0
		
		vector = Vector()
		vector.set_x_and_y(dx, dy)
				
		return vector
	
	""" gets a repulsive vector: find smallest distance to the obstacle:
	calculate distance to each corner and side of the obstacle, find nearest point.
	if the distance is to a line, theta = 90 (it's a perpendicular line)
	otherwise theta = the angle between the tank and the corner
	make theta tangential, then calculate dx, dy as with repulsive fields
	return a vector using dx, dy"""
	def get_obstacle_tangent_field(self, mytank, obj, r, s, b):
		
		d_edges, a_edges = self.__get_line_distances(mytank, obj)
		d_points = self.__get_point_distances(mytank, obj)
		
		d_close_edge = min(d_edges[0], d_edges[1], d_edges[2], d_edges[3])
		d_close_point = min(d_points[0], d_points[1], d_points[2], d_points[3])
		
		
		theta = a_edges[d_edges.index(d_close_edge)] #distance b/w line and point is perpendicular unless distance is to a corner
		if d_close_point == d_close_edge:
			corner = d_points.index(d_close_point)
			#theta = get_angle(mytank, Point(obj[corner]))
			#theta = theta  pi/2.0 #to make tangential
		
		dx = 0
		dy = 0
		
		if d_close_edge < r:
			dx = -sign(cos(theta))*float('inf')
			dy = -sign(sin(theta))*float('inf')
		elif d_close_edge >= r and d_close_edge <= s+r:
			dx = -b * (s + r - d_close_edge) * cos(theta)
			dy = -b * (s + r - d_close_edge) * sin(theta)
			
		vector = Vector()
		vector.set_x_and_y(dx, dy)
				
		return vector
		
	""" get all the tank's enemies, obstacles, and goals.
	calculate a potential field vector for each object:
	enemies => repulsive
	obstacles => tangential
	goals => attractive
	(goals are either flags or the agent's base)
	add all the potential vectors to find the desired vector, return it
	"""
	def get_desired_accel_vector(self, mytank, time_diff):
		
		team = [tank for tank in self.agent.mytanks if tank.index !=
						mytank.index]
		
		goal = self.agent.getTargetPoint(mytank, time_diff)
		#print "Tank ("+str(mytank.index)+") target: ("+ str(goal.x) +", "+ str(goal.y)+")       time diff: "+ str(time_diff)
						
		r = 1 #goal/obstacle radius
		s = 100 #goal/obstacle field radius
		a = 5 #attrctive force
		b = 3 #repulsive force
								
		vectors = []		
		
		vectors.append( self.get_attract_field(mytank, goal, r, s, a+4))
		
		obstacles = self.agent.grid.getObstacles()
		
		for obstacle in obstacles:
			vectors.append(self.get_obstacle_tangent_field(mytank, obstacle, r+5, s-85, a-1))	
		for tank in team:
			vectors.append(self.get_repulse_field(mytank, tank, r, s/10.0, b))
		"""
		for enemy in enemies:
			vectors.append(self.get_repulse_field(mytank, enemy, r+4, s/5.0, a+2))
		"""
		desired_vec = Vector(0,0)
		for vector in vectors:
			desired_vec = add_vectors(desired_vec, vector);
		#print "desiredVector. angle = "+ str(desired_vec.angle)
		
		return desired_vec
