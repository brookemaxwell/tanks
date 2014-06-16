#!/usr/bin/python -tt


import sys
import math
import time

import AimTankController
import EnemyKalmanController
import PFController

from HunterController import TankController as HunterController
from EnemyKalmanController import TankController as EnemyKalmanController
from PFController import PFTankController
from geometry import Vector, Point
from math import atan2, pi

from grid_prob import GridProbability
from bzrc_occ import BZRC, Command, Answer, UnexpectedResponse
from potential_field_occ import PotentialField

def getTimeInterval():
	return 4

NUM_OF_HUNTERS = 4;
NUM_OF_RUNNERS = 6;

class Agent(object):
	"""Class handles all command and control logic for a teams tanks."""

	def __init__(self, bzrc):
		self.bzrc = bzrc
		self.constants = self.bzrc.get_constants()
		self.commands = []
		self.hunterControllers = []
		self.runnerControllers = []
		self.distractorControllers = []
		self.targetControllers = []
		self.oldTime = 0
		self.lastTimeTargeted = -1
		self.grid = GridProbability()
		self.ourFlag ="?"
		
	def initialize(self):
		mytanks, othertanks, flags, shots, bases = self.bzrc.get_lots_o_stuff()
		self.mytanks = mytanks
		self.othertanks = othertanks
		self.enemies = [tank for tank in othertanks if tank.color !=
						self.constants['team']]
		
		if len(self.runnerControllers) == 0:
			if(len(mytanks) == 10):
				
				for tank in mytanks[0: NUM_OF_HUNTERS]:
					self.hunterControllers.append(HunterController(tank))
				for tank in mytanks[NUM_OF_HUNTERS : NUM_OF_HUNTERS + NUM_OF_RUNNERS]:
					self.runnerControllers.append(PFTankController(tank))

			elif(len(mytanks) == 2):
				for tank in mytanks[0: NUM_OF_HUNTERS]:
					self.hunterControllers.append(HunterController(tank))
				for tank in mytanks[NUM_OF_HUNTERS : NUM_OF_HUNTERS + NUM_OF_RUNNERS]:
					self.runnerControllers.append(PFTankController(tank))
			
			
			for othertank in self.enemies:
				self.targetControllers.append(EnemyKalmanController(othertank, getTimeInterval()))
				
	def updateControllers(self, time_diff):
		if len(self.runnerControllers) == 0:
			self.initialize();
		else:
			shooters = self.mytanks[0: NUM_OF_HUNTERS]
			runners = self.mytanks[NUM_OF_HUNTERS : NUM_OF_HUNTERS + NUM_OF_RUNNERS]
			
			for i in range (0, len(self.hunterControllers)):
				self.hunterControllers[i].tank = shooters[i]
			for i in range (0, len(self.runnerControllers)):
				self.runnerControllers[i].tank = runners[i]
			#update the TargetControllers
			for i in range (0, len(self.enemies)):
				self.targetControllers[i].tank = self.enemies[i]
			
			self.opponentColor = self.othertanks[0].color
			for i in range(0, len(self.flags)):
				if not self.flags[i].color == self.opponentColor:
					self.ourFlag = self.flags[i]
				

	#this code makes it so the targeting is running once every four seconds. 
	#It takes four seconds for a tank bullet to reach maxium distance and also to reload
	def tick(self, time_diff):
		#print "ticking "+ str(time_diff)
		
		#------------------  Set Up -------------------------------------------------
		self.commands = []
		
		"""Some time has passed; decide what to do next."""
		mytanks, othertanks, flags, shots, bases = self.bzrc.get_lots_o_stuff()
		self.mytanks = mytanks
		self.othertanks = othertanks
		self.flags = flags
		self.shots = shots
		self.bases = bases
		self.enemies = [tank for tank in othertanks if tank.color !=
						self.constants['team']]
		
		self.updateControllers(time_diff);
		
		#update everything
		self.updateHunters(time_diff);
		self.updateRunners(time_diff);
		results = self.bzrc.do_commands(self.commands)
	
	def updateRunners(self, time_diff):
		pf = PotentialField(self)
		
		self.obstacles = self.grid.getObstacles()
		
		for i in range(len(self.runnerControllers)):
			tankController = self.runnerControllers[i]
			#for tankController in self.tankControllers:
			
			
			if tankController.isAlive():
				tank = tankController.tank
				#update occ grid
				try:
					pos, curGrid = self.bzrc.get_occgrid(tank.index)
					self.grid.update_probabilities(curGrid, pos[0], pos[1])
				except UnexpectedResponse:
					print "caught error"
				
				#give tank directions
				desiredVector = pf.get_desired_accel_vector(tank, time_diff)
				cmd = tankController.getCommandFromVectors(desiredVector, time_diff)
				self.commands.append(cmd)
			
	def getRunnerTargetPoint(self, mytank):
		goal = self.flags[(mytank.index) %len(self.flags) ]# pick one flag goal
		if(self.flags[0].color == self.constants['team'] ):
			goal = self.flags[1]
		else:
			goal = self.flags[0]

		if mytank.flag != "-" or goal.poss_color == self.constants['team']:
			bases = self.bases
			bases = [base for base in bases if base.color ==
						self.constants['team']]
			if len(bases) == 1:
				base = bases[0]
				goal = Point(((base.corner1_x + base.corner3_x)/2.0, (base.corner1_y + base.corner3_y)/2.0))
				
		return goal

	def updateHunters(self, time_diff):
		#update the location of their tank only once a secon
		second = int(time_diff)
		if second != self.lastTimeTargeted:
			#update the targeting time
			self.lastTimeTargeted = second
			
			#update the TargetControllers
			for i in range (0, len(self.targetControllers)):
				self.targetControllers[i].updateTarget(self.enemies[i])	
		
		#feed our tanks continous commands
		for i in range (0, len(self.hunterControllers)):
			tankController = self.hunterControllers[i]
			
			#if the opponent has the flag, attack
			if self.opponenthasFlag():
				tankController.target = self.getFlagBearer()
			
			#otherwise attack the tank closets to the flag
			elif (not tankController.hasValidTarget()) and 8 < time_diff:
				tankController.target= self.getOpponentClosestToFlag()
				
			if tankController.hasValidTarget():
				cmd = tankController.getTargetingCommand()
				self.commands.append(cmd) 
		
		
		
	def opponenthasFlag(self):		
		return self.ourFlag.poss_color == self.opponentColor
		
		
		
		
			
	def getFlagBearer(self):
		closestController = self.targetControllers[0]
		closestDistance = 40000
		
		for i in range (0, len(self.targetControllers)):
			enemyController = self.targetControllers[i]
			if enemyController.isAlive():
				dist = dist2(enemyController.tank, self.ourFlag)
				if dist < closestDistance:
					closestDistance = dist
					closestController = enemyController
		return closestController
		
		
	def getOpponentClosestToFlag(self):
		closestController = self.targetControllers[0]
		closestDistance = 40000
		
		for i in range (0, len(self.targetControllers)):
			enemyController = self.targetControllers[i]
			if enemyController.isAlive():
				dist = dist2(enemyController.tank, self.ourFlag)
				if dist < closestDistance:
					closestDistance = dist
					closestController = enemyController

		return closestController

def dist2( v, w):
	return (v.x - w.x)**2 + (v.y - w.y)**2
	

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
