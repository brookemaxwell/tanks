from geometry import Vector
from math import atan2, pi
from bzrc import Command

"""A controller for a single tank. This used to be in the agent, but I wanted to clean up the agent code a tad so I made its own class"""
class TankController(object):
	
	def __init__(self, tank):
		self.prev_speed_error = 0
		self.prev_angle_error = 0
		self.tank = tank
		self.targetX = 0
		self.targetY = 0
		
	#TODO update the variables so that they make sense/are consistent (ex. speed_error and veolocityDiff)
	def getCommandFromVectors(self, desiredVector, timeDiff):	
		curTankAngle = self.getCurrentDirectionInPolar()
		#angleVel = desiredVector.angle - curTankVector.angle
		
		
		#intialize constants
		#Kp creates tight turns
		Kp = 1.0
		Kd = 0.0
		
		
		#magnitudeDiff = desiredVector.velocity - curVector.velocity
		angleDiff = desiredVector.angle - curTankAngle
		if abs(angleDiff + 2*pi) < abs(angleDiff):
			angleDiff = angleDiff + 2*pi
		elif abs(angleDiff - 2*pi) < abs(angleDiff):
			angleDiff = angleDiff - 2*pi
		
		#commandVector.velocity = Kp(velocityDiff) + Kd( velocityDiff - self.speed_error )/timeDiff
		#prevent a divide by zero error
		if timeDiff == 0:
			timeDiff = 0.01
		angleVel = Kp*angleDiff + Kd* (angleDiff - self.prev_angle_error )/timeDiff
		#speed_error = velocityDiff
		prev_angle_error = angleDiff
		
		
		if 1 < angleVel:
			angleVel = 1.0
		elif angleVel < -1: 
			angleVel = -1.0
		elif angleVel == 'nan':
			angleVel = 0
		"""				index, speed, angle, shoot"""
		return Command(self.tank.index, 0, .1, True)
		
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
	"""
	def aimAt(self, x, y):
		self.targetX = x
		self.targetY = y
	"""
	
