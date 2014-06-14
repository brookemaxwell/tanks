#!/usr/bin/python -tt

# Create Potential Field Vectors

from __future__ import division

import math
from math import sqrt,atan2,cos,sin,pi
import time

"""returns the square of a number"""
def sqr(x):  
	return x * x 
"""Make any angle be between +/- pi."""
def normalize_angle(angle):
	
	angle -= 2 * math.pi * int (angle / (2 * math.pi))
	if angle <= -math.pi:
		angle += 2 * math.pi
	elif angle > math.pi:
		angle -= 2 * math.pi
					
	if angle == 'nan':
		angle = 0
			
	return angle
""" calculates the angle(in radians) between two points"""
def get_angle(point1, point2):
	return atan2((point2.y-point1.y), (point2.x-point1.x))

""" calculates the distance from one object to another (as given in potential fields pdf)"""
def get_center_distance(mytank, obj):
	return sqrt(sqr(obj.x - mytank.x) + sqr(mytank.y - obj.y))

""" calculates the linear distance between two points"""
def get_distance(pt1, pt2):#x, y, x_o, y_o):
	return sqrt(dist2(pt1,pt2))

""" calculates the distance_squared between two points"""
def dist2( v, w):
	return sqr(v.x - w.x) + sqr(v.y - w.y) 

""" for simplification of code. calculates the distance_squared from a point to a line segment (two points)"""
def distToSegmentSquared( tank, v, w):#(p, v, w):
		
	l2 = dist2(v, w);
	if l2 == 0 :
		return dist2(tank, v);
	
	t = ((tank.x - v.x) * (w.x - v.x) + (tank.y - v.y) * (w.y - v.y)) / l2;
	
	if (t < 0):
		return dist2(tank, v);
	if (t > 1):
		return dist2(tank, w);
	
	return dist2(tank, Point((v.x + t * (w.x - v.x), v.y + t * (w.y - v.y))));

""" takes a a point and calculates the distance to a line segment (two points)"""
def distance_to_line(tank, p1, p2):
	return sqrt(distToSegmentSquared(tank, p1, p2));
	
def distance_and_perp_angle_to_line(tank, p1, p2):
	return (distance_to_line(tank, p1, p2), get_angle(p2, p1));

"""returns 1 for positive numbers, -1 for negative"""
def sign(num):
	if(num < 0):
		return -1
	return 1

"""adds two vectors together using their magnitudes and angles"""
def add_vectors(vec1, vec2):
	x1 = vec1.magnitude * cos(vec1.angle)
	y1 = vec1.magnitude * sin(vec1.angle)
   
	x2 = vec2.magnitude * cos(vec2.angle)
	y2 = vec2.magnitude * sin(vec2.angle)
	
	r_x = x1 + x2
	r_y = y1 + y2
	
	magnitude = sqrt(r_x*r_x + r_y*r_y)
	angle = atan2(r_y,r_x)
	
	return Vector(magnitude, angle)

""" vectors: committing crimes with direction(angle) and magnitude! """
class Vector(object):
	def __init__(self, magnitude=0, angle=0):
		self.magnitude = magnitude
		self.angle = angle
		
	def set_x_and_y(self, dx, dy):
		self.magnitude = sqrt(dx*dx + dy*dy)
		self.angle = atan2(dy,dx)
	
	def print_out(self):
		print "magnitude: " + str(self.magnitude) + ", angle: " + str(self.angle)

""" represents a point on a grid for easy math manipulation. get the point? """
class Point(object):

	def __init__(self, tuple_pt = (0,0)):
		self.x = tuple_pt[0]
		self.y = tuple_pt[1]
		
	def set_x_and_y(self, x, y):
		self.x = x
		self.y = y

	def set_point(self, tuple_pt):
		self.x = tuple_pt[0]
		self.y = tuple_pt[1]
	
	def print_out(self):
		print "x: " + str(self.x) + ", y: " + str(self.y)
