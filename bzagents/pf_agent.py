#!/usr/bin/python -tt


# This is the template for the pf agent. Right now it's just a copy of agent0.py


import sys
import math
import time

from bzrc import BZRC, Command
from potential_field import PotentialField

"""A controller for a single tank. """
class TankController(object):
	
	def __init__(self, tank):
		self.speed_error = 0
		self.angle_error = 0
		self.tank = tank
		
	#TODO update the variables so that they make sense/are consistent (ex. speed_error and veolocityDiff)
	def getCommandFromVectors(self, curVector, desiredVector, timeDiff):
		#intialize constants
		Kp = 0.1
		Kd = 0.5
		commandVector = Vector()
		velocityDiff = desiredVector.velocity - curVector.velocity
		#TODO how does this work with polar cooridantes or those returned by the potential_feild? Could we get strange behavoir with the angles overlapping
		angleDiff = desiredVector.angle - curVector.angle
		#TODO is timeDiff an int? Will dividing by timeDiff work?
		commandVector.velocity = Kp(velocityDiff) + Kd( velocityDiff - self.speed_error )/timeDiff
		commandVector.angle = Kp(angleDiff) + Kd( angleDiff - self.angle_error )/timeDiff
		speed_error = velocityDiff
		angle_error = angleDiff
		#TODO depending on how we get the angle and speed, convert these to a command
		"""					 index, speed, angle, shoot"""
		return Command(self.tank.index, 1, 0, True)
		
		
		
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
		mytanks, othertanks, flags, shots, obstacles = self.bzrc.get_lots_o_stuff()
		self.mytanks = mytanks
		self.othertanks = othertanks
		self.flags = flags
		self.shots = shots
		self.obstacles = obstacles
		self.enemies = [tank for tank in othertanks if tank.color !=
						self.constants['team']]

		self.commands = []
		
		#The tankControllers array assumes that tankController[1] will always correspond to mytanks[1]
		#if not intialized, intialize the tankController array
		if len(tankControllers) == 0:
			for tank in mytanks:
				tankControllers.append(TankController(tank))
		#else update the tank variable in each tank controller
		else:
			for i in range (0, len(tankControllers)):
				tankControllers[i].tank = mytanks[i]
		
		
		pf = PotentialField(self)
		
		
		print "before get desired acc vector"
		print "speed: " + str(pf.get_desired_accel_vector(mytanks[0]).velocity) + " angle: " + str(pf.get_desired_accel_vector(mytanks[0]).angle)
		print "after get desired acc vector"		

		
		for tankController in tankControllers:
			"""
			self.commands.append(Command(1, 1, 0, True))
			curVector = Vector(tank.vx, tank.vy)#TODO
			desiredAccelVector = potentialfield.getDesiredVector(tank)
			//handle acceraltion and angel changing vectors
			cmd = tankController.getCommandFromVectors(curVector, desiredVector, time_diff)
			self.commands.append(cmd)
			"""

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
