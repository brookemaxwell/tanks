#!/usr/bin/python -tt

""" 
Once you have the basic socket communication working build a really dumb agent. This agent should repeat the following forever:

Move forward for 3-8 seconds
Turn left about 60 degrees and then start going straight again
In addition to this movement your really dumb agent should also shoot every 2 seconds (random between 1.5 and 2.5 seconds) or so.


"""
#################################################################
# NOTE TO STUDENTS
# This is a starting point for you.  You will need to greatly
# modify this code if you want to do anything useful.  But this
# should help you to know how to interact with BZRC in order to
# get the information you need.
#
# After starting the bzrflag server, this is one way to start
# this code:
# python agent0.py [hostname] [port]
#
# Often this translates to something like the following (with the
# port name being printed out by the bzrflag server):
# python agent0.py localhost 49857
#################################################################

import sys
import math
import time

from bzrc import BZRC, Command

class Agent(object):
    """Class handles all command and control logic for a teams tanks."""

    def __init__(self, bzrc):
        self.bzrc = bzrc
        self.constants = self.bzrc.get_constants()
        self.commands = []

	#time diff is in seconds and is a float
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
		#---------------------MAIN LOGIC AREA------------------------
        
        #In addition to this movement your really dumb agent should also shoot every 2 seconds (random between 1.5 and 2.5 seconds) or so.
        shootCmd = time_diff % 2 <.1
        #Move forward for 5 seconds
        if time_diff % 10 < 5:
			self.commands = []
			for x in range(0, len(mytanks)):
				self.commands.append(Command(x, 1, 0, shootCmd))
        #stop for 2 seconds
        elif time_diff % 10 < 7:
			self.commands = []
			for x in range(0, len(mytanks)):
				self.commands.append(Command(x, 0, 0, shootCmd))
		#rotate for 1.5 sec
        elif time_diff % 10 < 8.5:
			self.commands = []
			for x in range(0, len(mytanks)):
				self.commands.append(Command(x, 0, 1, shootCmd))
        else:
			self.commands = []
			for x in range(0, len(mytanks)):
				self.commands.append(Command(x, 0, 0, shootCmd))
        
        #stop for 2 seconds
        #else:
		#	self.commands = [Command(1, -1, 0, shootCmd), Command(2, -1, 0, shootCmd)]
        #Reverse for 5 seconds
        
        #Move forward for 3-8 seconds
        
        
        #Turn left about 60 degrees and then start going straight again
        #In addition to this movement your really dumb agent should also shoot every 2 seconds (random between 1.5 and 2.5 seconds) or so.
		
		#A command has a tank, a speed, and angle, and a shoot command
        #self.commands = [Command(1, 1, .1, True), Command(2, 1, .1, True)]
		
        #for tank in mytanks:
        #   self.attack_enemies(tank)

        results = self.bzrc.do_commands(self.commands)
        #---------------------END MAIN LOGIC AREA------------------------
	

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
    #bzrc contains simply the connection (open the socket, connect to the game)
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
