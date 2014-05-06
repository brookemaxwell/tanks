#!/usr/bin/python -tt

# Create Potential Field Vectors

from __future__ import division

import math
from math import sqrt,atan2,cos,sin,pi
import time


class PotentialField:
	"""Class handles queries and responses with remote controled tanks."""

	def __init__(self, agent):
		self.agent = agent
 
	# Information Requests:

	def get_angle(self, x, y, x_o, y_o):
		return atan2((y_o-y), (x_o-x))	#atan2((y1-y2) / (x1-x2))?
	
	def get_center_distance(self, mytank, obj):
		return sqrt(pow(obj.x - mytank.x, 2) + pow(mytank.y - obj.y, 2))
	
	def get_distance(self, x, y, x_o, y_o):
		return sqrt(pow(x - x_o, 2) + pow(y_o - y, 2))
	
	def distance_to_line(self, linex1, linex2, liney1, liney2, x, y):
		# (x2-x1)x - (y2-y1)y - x1y2 + x2y1
		# ---------------------------------
		# sqrt ((x2-x1)^2 + (y2 - y1)^2) 
		
		x_d = ((linex2 - linex1) * x)
		y_d = ((liney2 - liney1) * y)
		
		return (x_d - y_d - linex1*liney2 + linex2 + liney1) / sqrt(x_d * x_d + y_d * y_d)
		
	def get_point_distances(self, mytank, obstacle):
		d1 = self.get_distance(obstacle[0][0], obstacle[0][1], 
								mytank.x, mytank.y)
		d2 = self.get_distance(obstacle[1][0], obstacle[1][1],
								mytank.x, mytank.y)
		d3 = self.get_distance(obstacle[2][0], obstacle[2][1],
								mytank.x, mytank.y)
		d4 = self.get_distance(obstacle[3][0], obstacle[3][1],
								mytank.x, mytank.y)
		
		return [d1, d2, d3, d4]
	
	def get_line_distances(self, mytank, obstacle):
		d1 = self.distance_to_line(obstacle[0][0], obstacle[1][0], 
								obstacle[0][1], obstacle[1][1], 
								mytank.x, mytank.y)
		d2 = self.distance_to_line(obstacle[1][0], obstacle[2][0], 
								obstacle[1][1], obstacle[2][1], 
								mytank.x, mytank.y)
		d3 = self.distance_to_line(obstacle[2][0], obstacle[3][0], 
								obstacle[2][1], obstacle[3][1], 
								mytank.x, mytank.y)
		d4 = self.distance_to_line(obstacle[3][0], obstacle[0][0], 
								obstacle[3][1], obstacle[0][1], 
								mytank.x, mytank.y)
								
		
		
		return [d1, d2, d3, d4]
		
	def sign(self, num):
		if(num < 0):
			return -1
		return 1

	def get_repulse_field(self, mytank, obj):
		"""get a repulsive vector"""
		r = 1#goal radius
		s = 100#field radius
		b = 1#attraction factor
		
		d = self.get_center_distance(mytank, obj)
		theta = self.get_angle(mytank.x, mytank.y, obj.x, obj.y)
		
		#then calc dx, dy based on d
		#return new vector(dx, dy)?
		dx = 0
		dy = 0
		
		if d < r:
			dx = -self.sign(cos(theta))*float('inf')
			dy = -self.sign(sin(theta))*float('inf')
		elif d >= r and d <= s+r:
			dx = -b * (s + r - d) * cos(theta)
			dy = -b * (s + r - d) * sin(theta)
			
		#else dx, dy = 0
				
		vector = Vector()
		vector.set_x_and_y(dx, dy)
				
		return vector

	def get_attract_field(self, mytank, obj):
		"""get an attractive vector"""
		r = 1#goal radius
		s = 100#field radius
		a = 1#attraction factor
		
		d = self.get_center_distance(mytank, obj)
		theta = self.get_angle(mytank.x, mytank.y, obj.x, obj.y)
		#then calc dx, dy based on d
		#return new vector(dx, dy)?
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
		
	def get_obstacle_tangent_field(self, mytank, obj):
		r = 1#goal radius
		s = 100#field radius
		b = 1#repulisve factor
		
		"""get a tngential vector"""
		d_edges = self.get_line_distances(mytank, obj)
		d_points = self.get_point_distances(mytank, obj)
		
		d_close_edge = min(d_edges[0], d_edges[1], d_edges[2], d_edges[3])
		d_close_point = min(d_points[0], d_points[1], d_points[2], d_points[3])
		
		theta = pi/2.0 #distance b/w line and point is perpendicular unless distance is to a corner
		if d_close_point == d_close_edge:
			corner = d_points.index(d_close_point)
			o_x = obj["corner"+str(corner)+"_x"]
			o_y = obj["corner"+str(corner)+"_y"]
			theta = self.get_angle(mytank.x,mytank.y, o_x, o_y)
			
		#then calc dx, dy based on d_close_edge
		#return new vector(dx, dy)?
		
		theta = theta + pi/2.0 #to make tangential
		
		dx = 0
		dy = 0
		
		if d_close_edge < r:
			dx = -self.sign(cos(theta))*float('inf')
			dy = -self.sign(sin(theta))*float('inf')
		elif d_close_edge >= r and d_close_edge <= s+r:
			dx = -b * (s + r - d_close_edge) * cos(theta)
			dy = -b * (s + r - d_close_edge) * sin(theta)
			
		vector = Vector()
		vector.set_x_and_y(dx, dy)
				
		return vector

	def add_vectors(self, vec1, vec2):
		"""add two vectors together"""
		x1 = vec1.velocity * cos(vec1.angle)
		y1 = vec1.velocity * sin(vec1.angle)
	   
		x2 = vec2.velocity * cos(vec2.angle)
		y2 = vec2.velocity * sin(vec2.angle)
		
		r_x = x1 + x2
		r_y = y1 + y2
		
		velocity = sqrt(r_x*r_x + r_y*r_y)
		angle = atan2(r_y,r_x)
		
		return Vector(velocity, angle)
	
	def get_desired_accel_vector(self, mytank):
		"""get an attractive vector"""
		enemies = self.agent.enemies
		obstacles = self.agent.obstacles
		flags = self.agent.flags
		goals = [flag for flag in flags if flag.color !=
						self.agent.constants['team']]
		if mytank.flag != "-":
			bases = self.agent.bases
			goals = [base for base in bases if base.color ==
						self.agent.constants['team']]		
		
		vectors = []		
		for goal in goals:
			vectors.append( self.get_attract_field(mytank, goal))
		for obstacle in obstacles:
			vectors.append(self.get_obstacle_tangent_field(mytank, obstacle))
		for enemy in enemies:
			vectors.append(self.get_repulse_field(mytank, enemy))
		
		
		desired_vec = Vector(0,0)
		for vector in vectors:
			desired_vec = self.add_vectors(desired_vec, vector);
		
		return desired_vec



class Vector(object):
	"""Class for setting a command for a tank."""

	def __init__(self, velocity=0, angle=0):
		self.velocity = velocity
		self.angle = angle
		
	def set_x_and_y(self, dx, dy):
		self.velocity = sqrt(dx*dx + dy*dy)
		self.angle = atan2(dy,dx)
	


