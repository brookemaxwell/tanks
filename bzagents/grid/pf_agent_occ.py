#!/usr/bin/python -tt


# This is the template for the pf agent. Right now it's just a copy of agent0.py


import sys
import math
import time
import grid_drawer

from grid_prob import GridProbability
from bzrc_occ import BZRC, Command, Answer
from potential_field_occ import PotentialField
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
	
		
	

class Agent(object):
	"""Class handles all command and control logic for a teams tanks."""

	def __init__(self, bzrc):
		self.bzrc = bzrc
		self.constants = self.bzrc.get_constants()
		self.commands = []
		self.tankControllers = []
		self.oldTime = 0
		#create an array so that no tanks get the same cooridnate to go to, used after 130 seconds
		#There is a sexy python sytanx for these next two lines no?
		self.lastTargets = []
		for i in range(10):
			self.lastTargets.append(Answer())
		self.grid = GridProbability()
		grid_drawer.init_window(800,800)
		

	def tick(self, time_diff):
		"""Some time has passed; decide what to do next."""
		mytanks, othertanks, flags, shots, bases = self.bzrc.get_lots_o_stuff()
		self.mytanks = mytanks
		self.othertanks = othertanks
		self.flags = flags
		self.shots = shots
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
		
		self.obstacles = self.grid.getObstacles()
		
		
		
		for i in range(len(self.tankControllers)):
			tankController = self.tankControllers[i]
			#for tankController in self.tankControllers:
			tank = tankController.tank
			
			#update occ grid
			pos, curGrid = self.bzrc.get_occgrid(tank.index)
			
			self.grid.update_probabilities(curGrid, pos[0], pos[1])
			
			#give tank directions
			desiredVector = pf.get_desired_accel_vector(tank, time_diff)
			cmd = tankController.getCommandFromVectors(desiredVector, time_diff)
			self.commands.append(cmd)
					
		grid_drawer.update_grid(self.grid.prob_grid)
		grid_drawer.draw_grid()
		results = self.bzrc.do_commands(self.commands)


	def getTargetPoint(self, tank, time_diff):
		answer = Answer()
		#assign each tank a row
		yCoorAssigned = tank.index*80-399
		answer.y = yCoorAssigned
		
		#for the first twenty five seconds, just get tanks to their points
		if time_diff < 25:
			answer.x = -399
		#for every ten seconds, move their goal over 100 pixels
		elif 25 < time_diff and time_diff < 130:
			lengthOfPhase = 130- 25
			phase = (time_diff-25)/lengthOfPhase
			targetX = phase*799 -399
			answer.x = targetX
		#by this point, the tanks have crossed the grid, now send them to clean some unscanned spots up
		else:
			#every 40 seconds get a new target
			if (time_diff-130) % 40 < 1 :
				self.lastTargets = []
				for i in range(10):
					self.lastTargets.append(Answer())
				answer = self.grid.getRandomUnknownPoint(tank)
				self.lastTargets[tank.index] = answer
			elif not hasattr(self.lastTargets[tank.index], 'x'):
				answer = self.grid.getRandomUnknownPoint(tank)
				self.lastTargets[tank.index] = answer
			else:
				answer = self.lastTargets[tank.index]
			
		return answer
			


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
