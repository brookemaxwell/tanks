#!/usr/bin/python -tt


# This is the template for the pf agent. Right now it's just a copy of agent0.py


import sys
import math
import time

from bzrc import BZRC, Command
from potential_field import PotentialField
from geometry import Vector
from math import atan2, pi

"""A controller for a single tank. """
class TankController(object):
	
	def __init__(self, tank):
		self.prev_speed_error = 0
		self.prev_angle_error = 0
		self.tank = tank
		
	#TODO update the variables so that they make sense/are consistent (ex. speed_error and veolocityDiff)
	def getCommandFromVectors(self, desiredVector, timeDiff):	
		curTankAngle = self.getCurrentDirectionInPolar()
		#angleVel = desiredVector.angle - curTankVector.angle
		
		
		#intialize constants
		#Kp creates tight turns
		Kp = 1.0
		Kd = 0.0
		
		
		#magnitudeDiff = desiredVector.velocity - curVector.velocity
		#TODO how does this work with polar cooridantes or those returned by the potential_feild? Could we get strange behavoir with the angles overlapping
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
			angleVel = 1.0
		elif angleVel < -1: 
			angleVel = -1.0
		elif angleVel == 'nan':
			angleVel = 0
		"""					 index, speed, angle, shoot"""
		return Command(self.tank.index, 1, angleVel, True)
		
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
	
		
	

class Agent(object):
	"""Class handles all command and control logic for a teams tanks."""

	def __init__(self, bzrc):
		self.bzrc = bzrc
		self.constants = self.bzrc.get_constants()
		self.commands = []
		self.tankControllers = []
		self.oldTime = 0
		

	def tick(self, time_diff):
		"""Some time has passed; decide what to do next."""
		mytanks, othertanks, flags, shots, obstacles, bases = self.bzrc.get_lots_o_stuff()
		self.mytanks = mytanks
		self.othertanks = othertanks
		self.flags = flags
		self.shots = shots
		self.obstacles = obstacles
		self.bases = bases
		self.enemies = [tank for tank in othertanks if tank.color !=
						self.constants['team']]

		self.commands = []
	
		#The tankControllers array assumes that tankController[1] will always correspond to mytanks[1]
		#if not intialized, intialize the tankController array
		if len(self.tankControllers) == 0:
			for tank in mytanks:
				self.tankControllers.append(TankController(tank))
		#else update the tank variable in each tank controller
		else:
			for i in range (0, len(self.tankControllers)):
				self.tankControllers[i].tank = mytanks[i]
		
		
		pf = PotentialField(self)
		
		for tankController in self.tankControllers:
			tank = tankController.tank
			desiredVector = pf.get_desired_accel_vector(tank)
			cmd = tankController.getCommandFromVectors(desiredVector, time_diff)
			self.commands.append(cmd)			

		results = self.bzrc.do_commands(self.commands)


	def attack_enemies(self, tank):
		"""Find the closest enemy and chase it, shooting as you go."""
		best_enemy = None
		best_dist = 2 * float(self.constants['worldsize'])
		for enemy in self.enemies:
			if enemy.status != 'alive':
				continue
			dist = math.sqrt((enemy.x - tank.x)**2 + (enemy.y - tank.y)**2)
			if dist < best_dist:
				best_dist = dist
				best_enemy = enemy
		if best_enemy is None:
			command = Command(tank.index, 0, 0, False)
			self.commands.append(command)
		else:
			self.move_to_position(tank, best_enemy.x, best_enemy.y)

	def move_to_position(self, tank, target_x, target_y):
		"""Set command to move to given coordinates."""
		target_angle = math.atan2(target_y - tank.y,
								  target_x - tank.x)
		relative_angle = self.normalize_angle(target_angle - tank.angle)
		command = Command(tank.index, 1, 2 * relative_angle, True)
		self.commands.append(command)

	def normalize_angle(self, angle):
		"""Make any angle be between +/- pi."""
		angle -= 2 * math.pi * int (angle / (2 * math.pi))
		if angle <= -math.pi:
			angle += 2 * math.pi
		elif angle > math.pi:
			angle -= 2 * math.pi
		return angle


def main():
	# Process CLI arguments.
	try:
		execname, host, port = sys.argv
	except ValueError:
		execname = sys.argv[0]
		print >>sys.stderr, '%s: incorrect number of arguments' % execname
		print >>sys.stderr, 'usage: %s hostname port' % sys.argv[0]
		sys.exit(-1)

	# Connect.
	#bzrc = BZRC(host, int(port), debug=True)
	bzrc = BZRC(host, int(port))

	agent = Agent(bzrc)

	prev_time = time.time()

	# Run the agent
	try:
		while True:
			time_diff = time.time() - prev_time
			agent.tick(time_diff)
	except KeyboardInterrupt:
		print "Exiting due to keyboard interrupt."
		bzrc.close()


if __name__ == '__main__':
	main()

# vim: et sw=4 sts=4
