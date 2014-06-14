#!/usr/bin/python -tt


import sys
import math
import time

from AimTankController import AimTankController
from KalmanEnemyController import KalmanEnemyController
from PFController import PFTankController
from bzrc import BZRC, Command
from geometry import Vector
from math import atan2, pi

from grid_prob import GridProbability
from bzrc_occ import BZRC, Command, Answer
from potential_field_occ import PotentialField

def getTimeInterval():
	return 4

NUM_OF_SHOOTERS = 2;
NUM_OF_DISTRACTORS = 2;
NUM_OF_RUNNERS = 6;

class Agent(object):
	"""Class handles all command and control logic for a teams tanks."""

	def __init__(self, bzrc):
		self.bzrc = bzrc
		self.constants = self.bzrc.get_constants()
		self.commands = []
		self.shooterControllers = []
		self.runnerControllers = []
		self.distractorControllers = []
		self.targetControllers = []
		self.oldTime = 0
		self.lastTimeTargeted = -1
		self.grid = GridProbability()
		
	def initialize():
		mytanks, othertanks, flags, shots, obstacles, bases = self.bzrc.get_lots_o_stuff()
		self.mytanks = mytanks
		self.othertanks = othertanks
		self.enemies = [tank for tank in othertanks if tank.color !=
						self.constants['team']]
		
		if len(self.tankControllers) == 0:
			if(len(mytanks) == 10):
				
				for tank in mytanks[0: NUM_OF_SHOOTERS]:
					self.shooterControllers.append(AimTankController(tank))
				for tank in mytanks[NUM_OF_SHOOTERS : NUM_OF_SHOOTERS + NUM_OF_RUNNERS]:
					self.runnerControllers.append(PFTankController(tank))
				for tank in mytanks[NUM_OF_SHOOTERS + NUM_OF_RUNNERS: len(mytanks)]
					self.distractorControllers.append(TankController(tank))#this one doesn't exist yet
				
			for othertank in self.enemies:
				self.targetControllers.append(EnemyKalmanController(othertank, getTimeInterval()))
				
	def updateControllers():
		if len(self.tankControllers) == 0:
			self.initialize();
		else:
			for i in range (0, len(self.tankControllers)):
				self.tankControllers[i].tank = mytanks[i]

	#this code makes it so the targeting is running once every four seconds. 
	#It takes four seconds for a tank bullet to reach maxium distance and also to reload
	def tick(self, time_diff):
		
		#------------------  Set Up -------------------------------------------------
		self.commands = []
		
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
		
		self.updateControllers();
		
		#update everything
		self.updateShooters(time_diff);
		self.updateRunners(time_diff);
		results = self.bzrc.do_commands(self.commands)
	
	def updateRunners(self, time_diff):
		pf = PotentialField(self)
		
		self.obstacles = self.grid.getObstacles()
		
		for i in range(len(self.runnerControllers)):
			tankController = self.runnerControllers[i]
			#for tankController in self.tankControllers:
			tank = tankController.tank
			
			#update occ grid
			pos, curGrid = self.bzrc.get_occgrid(tank.index)
			
			self.grid.update_probabilities(curGrid, pos[0], pos[1])
			
			#give tank directions
			desiredVector = pf.get_desired_accel_vector(tank, time_diff)
			cmd = tankController.getCommandFromVectors(desiredVector, time_diff)
			self.commands.append(cmd)
			
	def getRunnerTargetPoint(self, mytank):
				
		goal = flags[(mytank.index) %len(flags) ]# pick one flag goal
		if mytank.flag != "-" or goal.poss_color == self.constants['team']:
			bases = self.bases
			bases = [base for base in bases if base.color ==
						self.constants['team']]
			if len(bases) == 1:
				base = bases[0]
				goal = Point(((base.corner1_x + base.corner3_x)/2.0, (base.corner1_y + base.corner3_y)/2.0))
				
		return goal

	def updateShooters(self, time_diff):
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
			for i in range (0, len(self.shooterControllers)):
				tankController = self.shooterControllers[i]
				
				#get this tanks target controller: the nearest one...
				target = self.targetControllers[0]
				
				tankController.updateTarget(target)				
				cmd = tankController.getFireCommand()
				self.commands.append(cmd) 

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
	
	agent.initialize();

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
