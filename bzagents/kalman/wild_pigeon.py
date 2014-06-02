#!/usr/bin/python -tt

#####################
#
#logic for clay pigeons: one wild(unpredictable), one moving predictably, and one stationary.
#
#####################
import sys
import math
import time

from bzrc import BZRC, Command

class WildPigeonAgent(object):
    """Class handles all command and control logic for a wild clay pigeon tank team."""

    def __init__(self, bzrc):
        self.bzrc = bzrc
        self.constants = self.bzrc.get_constants()
        self.commands = []

	#time diff is in seconds and is a float
    def tick(self, time_diff):
        mytanks, othertanks, flags, shots, obstacles, bases = self.bzrc.get_lots_o_stuff()
		#---------------------MAIN LOGIC AREA------------------------
        
        # speed 1 for 5 seconds, turning one way.
        if time_diff % 10 < 5:
			self.commands = []
			for x in range(0, len(mytanks)):
				self.commands.append(Command(x, 1, .5, False))
        #speed .5 for 4 seconds, turning other way.
        elif time_diff % 10 < 9:
			self.commands = []
			for x in range(0, len(mytanks)):
				self.commands.append(Command(x, .5, -1, False))
		

        results = self.bzrc.do_commands(self.commands)
        #---------------------END MAIN LOGIC AREA------------------------

class PigeonAgent(object):
	"""Class handles all command and control logic for a predictably moving clay pigeon tank team."""

	def __init__(self, bzrc):
		self.bzrc = bzrc
		self.constants = self.bzrc.get_constants()
		self.commands = []

	#time diff is in seconds and is a float
	def tick(self, time_diff):
		mytanks, othertanks, flags, shots, obstacles, bases = self.bzrc.get_lots_o_stuff()
		"""Some time has passed; decide what to do next."""
		#---------------------MAIN LOGIC AREA------------------------
		for x in range(0, len(mytanks)):
			self.commands.append(Command(x, 1, 0, False))
		results = self.bzrc.do_commands(self.commands)

class StationaryPigeonAgent(object):
	"""Class handles all command and control logic for a stationary clay pigeon tank team (aka, none)."""

	def __init__(self, bzrc):
		self.bzrc = bzrc
		self.constants = self.bzrc.get_constants()
		self.commands = []

	#time diff is in seconds and is a float
	def tick(self, time_diff):
		mytanks, othertanks, flags, shots, obstacles, bases = self.bzrc.get_lots_o_stuff()
		"""don't do anything, just sit there."""

def main():
    # Process CLI arguments.
    try:
        execname, host, port = sys.argv
    except ValueError:
        execname = sys.argv[0]
        print >>sys.stderr, '%s: incorrect number of arguments' % execname
        print >>sys.stderr, 'usage: %s hostname port' % sys.argv[0]
        sys.exit(-1)
        
    bzrc = BZRC(host, int(port))

    agent = WildPigeonAgent(bzrc)

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
