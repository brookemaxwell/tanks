from geometry import Vector, normalize_angle
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
		self.target = 0
	
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
	
	def getFireCommand(self):
		"""				index, speed, angle, shoot"""
		return Command(self.tank.index, 0, 0, True)
		
	def updateTarget(self, targetCont):
		self.target = targetCont
		self.targetX, self.targetY = self.target.getTargetPosAtNextInterval()
		
	
	def getTargetingCommand(self, time_diff):
		yDiff = self.targetY - self.tank.y
		xDiff = self.targetX - self.tank.x
		
		target_angle = atan2(yDiff, xDiff)
		relative_angle = normalize_angle(target_angle - self.tank.angle)
		
		shoot = False
		angleVel = relative_angle * 2#/time_diff
			
		return Command(self.tank.index, 0, angleVel, shoot)
		
	
