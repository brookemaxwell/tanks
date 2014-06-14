#!/usr/bin/python -tt

# This is the controller for a potential field runner

import sys
import math
import time

from grid_prob import GridProbability
from bzrc_occ import BZRC, Command, Answer
from potential_field_occ import PotentialField
from geometry import Vector
from math import atan2, pi

"""A controller for a single tank. """
class PFTankController(object):
	
	def __init__(self, tank):
		self.prev_speed_error = 0
		self.prev_angle_error = 0
		self.tank = tank
	
	#TODO update the variables so that they make sense/are consistent (ex. speed_error and veolocityDiff)
	def getCommandFromVectors(self, desiredVector, timeDiff):	
		curTankAngle = self.getCurrentDirectionInPolar()
		
		#intialize constants
		#Kp creates tight turns
		Kp = .9
		Kd = 0.1
		
		angleDiff = desiredVector.angle - curTankAngle
		if abs(angleDiff + 2*pi) < abs(angleDiff):
			angleDiff = angleDiff + 2*pi
		elif abs(angleDiff - 2*pi) < abs(angleDiff):
			angleDiff = angleDiff - 2*pi
		#TODO is timeDiff an int? Will dividing by timeDiff work?
		#commandVector.velocity = Kp(velocityDiff) + Kd( velocityDiff - self.speed_error )/timeDiff
		#prevent a divide by zero error
		if timeDiff == 0:
			timeDiff = 0.01
		angleVel = Kp*angleDiff + Kd* (angleDiff - self.prev_angle_error )/timeDiff
		#speed_error = velocityDiff
		prev_angle_error = angleDiff
		#TODO depending on how we get the angle and speed, convert these to a command
		
		if 1 < angleVel:
			angleVel = 1
		elif angleVel < -1: 
			angleVel = -1
		elif angleVel == 'nan':
			angleVel = 0
		"""					 index, speed, angle, shoot"""
		return Command(self.tank.index, .7, angleVel, True)
		
	"""Returns the tanks direction of movment in polar coordinates. It uses the  tank x and y velocity to do so"""	
	def getCurrentDirectionInPolar(self):
		vx = self.tank.vx
		vy = self.tank.vy
		
		#the follow statement prevents divide by zero errors
		if vx == 0 and vy == 0:
			return 0
		elif vx == 0 and 0 < vy:
			return pi/2
		elif vx == 0 and vy < 0:
			return 3*pi/2
		else:		
			return atan2(vy,vx)
