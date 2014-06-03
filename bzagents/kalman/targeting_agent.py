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
		

	#this code makes it so the targeting is running once every four seconds. 
	#It takes four seconds for a tank bullet to reach maxium distance and also to reload
	def tick(self, time_diff):
		
		#------------------  Set Up -------------------------------------------------
		self.commands = []
		
		"""Some time has passed; decide what to do next."""
		mytanks, othertanks, flags, shots, obstacles, bases = self.bzrc.get_lots_o_stuff()
		self.mytanks = mytanks
		self.othertanks = othertanks
		#self.flags = flags
		#self.shots = shots
		#self.obstacles = obstacles
		#self.bases = bases
		self.enemies = [tank for tank in othertanks if tank.color !=
						self.constants['team']]
		
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
		
		#position tank based on latest observation
		second = int(time_diff)
		
		#------------------  if still aiming-------------------------------------------------
		if second == self.lastTimeTargeted or second%getTimeInterval() != 0:
			for i in range (0, len(self.tankControllers)):
				cmd = self.tankControllers[i].getTargetingCommand(second)
				self.commands.append(cmd) 
		
		#------------------ if time to update the target and fire again-------------------------------------------------
		else:
			#update last time targeteted
			self.lastTimeTargeted = second
			#print self.lastTimeTargeted
			
			#update the TargetControllers
			for i in range (0, len(self.targetControllers)):
				self.targetControllers[i].updateTarget(othertanks[i])
			
			#plot the plot
			if self.lastTimeTargeted!=0:
				for tank in mytanks:
					sigma_x = self.targetControllers[0].Et.item((0,0));
					sigma_y = self.targetControllers[0].Et.item((3,3));
					target_x = self.targetControllers[0].mewt.item((0,0));
					target_y = self.targetControllers[0].mewt.item((3,0)); 
					plt.plot(tank, sigma_x, sigma_y, target_x, target_y)
			
			#update our tank controllers
			for i in range (0, len(self.tankControllers)):
				tankController = self.tankControllers[i]
				
				#get this tanks target controller
				if i < len(self.targetControllers):
					target = self.targetControllers[i]
				else:
					target = self.targetControllers[0]
				
				tankController.updateTarget(target)				
				cmd = tankController.getFireCommand()
				self.commands.append(cmd)			

		results = self.bzrc.do_commands(self.commands)
		
		
		


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
