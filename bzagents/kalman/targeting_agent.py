#!/usr/bin/python -tt


import sys
import math
import time

from TankController import TankController
from TargetController import TargetController
from bzrc import BZRC, Command
from geometry import Vector
from math import atan2, pi
import density_plot as plt

def getTimeInterval():
	return 4


class Agent(object):
	"""Class handles all command and control logic for a teams tanks."""

	def __init__(self, bzrc):
		self.bzrc = bzrc
		self.constants = self.bzrc.get_constants()
		self.commands = []
		self.tankControllers = []
		self.targetControllers = []
		self.oldTime = 0
		self.lastTimeTargeted = -1
		

	def tick(self, time_diff):
		#this code makes it so the targeting is running once every four seconds. 
		#It takes four seconds for a tank bullet to reach maxium distance and also to reload
		
		#position tank based on latest observation
		
		second = int(time_diff)
		if second == self.lastTimeTargeted or second%getTimeInterval() != 0:
			mytanks = self.bzrc.get_mytanks
			for tank in mytanks:
				sigma_x = self.targetControllers[0].Et.item((0,0));
				sigma_y = self.targetControllers[0].Et.item((3,3));
				plt.plot(tank, sigma_x, sigma_y)
			return
		self.lastTimeTargeted = second
		
		print self.lastTimeTargeted
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
		#if not intialized, intialize the tankControllers and targetControllers array
		if len(self.tankControllers) == 0:
			for tank in mytanks:
				self.tankControllers.append(TankController(tank))
			for othertank in othertanks:
				self.targetControllers.append(TargetController(othertank, getTimeInterval()))
		#else update the tank variable in each tank and target controller
		else:
			for i in range (0, len(self.tankControllers)):
				self.tankControllers[i].tank = mytanks[i]
			for i in range (0, len(self.targetControllers)):
				self.targetControllers[i].updateTarget(othertanks[i])
		
		
		for i in range (0, len(self.tankControllers)):
			tankController = self.tankControllers[i]
			
			#get this tanks target controller
			if i < len(self.targetControllers):
				target = self.targetControllers[i]
			else:
				target = self.targetControllers[0]
			
			self.targetControllers[i].getTargetPosAtNextInterval()
			
			desiredVector = Vector(0,0)
			
			
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
