#!/usr/bin/python -tt

# Create Potential Field Vectors

from __future__ import division

import math
import time


class PotentialField:
    """Class handles queries and responses with remote controled tanks."""

    def __init__(self, agent):
		self.agent = agent
 
'''
    def read_teams(self):
        """Get team information."""
        self.expect('begin')
        teams = []
        while True:
            i, rest = self.expect_multi(('team',),('end',))
            if i == 1:
                break
            team = Answer()
            team.color = rest[0]
            team.count = float(rest[1])
            team.base = [(float(x), float(y)) for (x, y) in
                    zip(rest[2:10:2], rest[3:10:2])]
            teams.append(team)
        return teams

    def read_obstacles(self):
        """Get obstacle information."""
        self.expect('begin')
        obstacles = []
        while True:
            i, rest = self.expect_multi(('obstacle',),('end',))
            if i == 1:
                break
            obstacle = [(float(x), float(y)) for (x, y) in
                    zip(rest[::2], rest[1::2])]
            obstacles.append(obstacle)
        return obstacles

    def read_occgrid(self):
        """Read grid."""
        response = self.read_arr()
        if 'fail' in response:
            return None
        pos = tuple(int(a) for a in self.expect('at')[0].split(','))
        size = tuple(int(a) for a in self.expect('size')[0].split('x'))
        grid = [[0 for i in range(size[1])] for j in range(size[0])]
        for x in range(size[0]):
            line = self.read_arr()[0]
            for y in range(size[1]):
                if line[y] == '1':
                    grid[x][y] = 1
        self.expect('end', True)
        return pos, grid

    def read_flags(self):
        """Get flag information."""
        line = self.read_arr()
        if line[0] != 'begin':
            self.die_confused('begin', line)

        flags = []
        while True:
            line = self.read_arr()
            if line[0] == 'flag':
                flag = Answer()
                flag.color = line[1]
                flag.poss_color = line[2]
                flag.x = float(line[3])
                flag.y = float(line[4])
                flags.append(flag)
            elif line[0] == 'end':
                break
            else:
                self.die_confused('flag or end', line)
        return flags

    def read_shots(self):
        """Get shot information."""
        line = self.read_arr()
        if line[0] != 'begin':
            self.die_confused('begin', line)

        shots = []
        while True:
            line = self.read_arr()
            if line[0] == 'shot':
                shot = Answer()
                shot.x = float(line[1])
                shot.y = float(line[2])
                shot.vx = float(line[3])
                shot.vy = float(line[4])
                shots.append(shot)
            elif line[0] == 'end':
                break
            else:
                self.die_confused('shot or end', line)
        return shots

    def read_mytanks(self):
        """Get friendly tank information."""
        line = self.read_arr()
        if line[0] != 'begin':
            self.die_confused('begin', line)

        tanks = []
        while True:
            line = self.read_arr()
            if line[0] == 'mytank':
                tank = Answer()
                tank.index = int(line[1])
                tank.callsign = line[2]
                tank.status = line[3]
                tank.shots_avail = int(line[4])
                tank.time_to_reload = float(line[5])
                tank.flag = line[6]
                tank.x = float(line[7])
                tank.y = float(line[8])
                tank.angle = float(line[9])
                tank.vx = float(line[10])
                tank.vy = float(line[11])
                tank.angvel = float(line[12])
                tanks.append(tank)
            elif line[0] == 'end':
                break
            else:
                self.die_confused('mytank or end', line)
        return tanks

    def read_othertanks(self):
        """Get enemy tank information."""
        line = self.read_arr()
        if line[0] != 'begin':
            self.die_confused('begin', line)

        tanks = []
        while True:
            line = self.read_arr()
            if line[0] == 'othertank':
                tank = Answer()
                tank.callsign = line[1]
                tank.color = line[2]
                tank.status = line[3]
                tank.flag = line[4]
                tank.x = float(line[5])
                tank.y = float(line[6])
                tank.angle = float(line[7])
                tanks.append(tank)
            elif line[0] == 'end':
                break
            else:
                self.die_confused('othertank or end', line)
        return tanks

    def read_bases(self):
        """Get base information."""
        bases = []
        line = self.read_arr()
        if line[0] != 'begin':
            self.die_confused('begin', line)
        while True:
            line = self.read_arr()
            if line[0] == 'base':
                base = Answer()
                base.color = line[1]
                base.corner1_x = float(line[2])
                base.corner1_y = float(line[3])
                base.corner2_x = float(line[4])
                base.corner2_y = float(line[5])
                base.corner3_x = float(line[6])
                base.corner3_y = float(line[7])
                base.corner4_x = float(line[8])
                base.corner4_y = float(line[9])
                bases.append(base)
            elif line[0] == 'end':
                break
            else:
                self.die_confused('othertank or end', line)
        return bases

    def read_constants(self):
        """Get constants."""
        line = self.read_arr()
        if line[0] != 'begin':
            self.die_confused('begin', line)

        constants = {}
        while True:
            line = self.read_arr()
            if line[0] == 'constant':
                constants[line[1]] = line[2]
            elif line[0] == 'end':
                break
            else:
                self.die_confused('constant or end', line)
        return constants
'''

    # Information Requests:

    def get_tangent_field(self, mytank, obj):
        """get a tngential vector"""
       
        return 

    def get_repulse_field(self, mytank, obj):
        """get a repulsive vector"""
        
        return

    def get_attract_field(self, mytank, obj):
        """get an attractive vector"""
        
        return 

    def add_vectors(self, vec1, vec2):
        """add two vectors together"""
        
        return
    
    def get_desired_vector(self, mytank):
        """get an attractive vector"""
        #self.agent.enemies
        
        
        return



class Vector(object):
    """Class for setting a command for a tank."""

    def __init__(self, velocity, angle):
        self.velocity = velocity
        self.angle = angle
        
    #def __init__(self, vx, vy):
		#self.velocity = calculate...
		#self.angle = calculate...


