#!/usr/bin/python -tt

# Create Multivariate density plot

from __future__ import division

import geometry
import numpy as np

from math import cos,sin,pi	

def printHeader():
	
	s = "set xrange [-400.0: 400.0]"+ "\n"
	s = s + "set yrange [-400.0: 400.0]"+ "\n"
	s = s + "set pm3d"+ "\n"
	s = s + "set view map"+ "\n"
	s = s + "unset key"+ "\n"
	s = s + "set size square"+ "\n"
	return s
	
#this sets the range of the density function (?). right now it doesn't actually do more than the demo
def printArrows(x, y, radius):
	s = "unset arrow" + "\n"
	s = s + "set arrow from "+str(x - radius) + ", "+str(y - radius)+" to "+str(x - radius) + ", "+str(y + radius) +" nohead front lt 3" + "\n"
	s = s + "set arrow from "+str(x - radius) + ", "+str(y - radius)+" to "+str(x + radius) + ", "+str(y - radius) +" nohead front lt 3" + "\n"
	s = s + "set arrow from "+str(x - radius) + ", "+str(y + radius)+" to "+str(x + radius) + ", "+str(y + radius) +" nohead front lt 3"+ "\n"
	s = s + "set arrow from "+str(x + radius) + ", "+str(y - radius)+" to "+str(x + radius) + ", "+str(y + radius) +" nohead front lt 3"+ "\n"
	return s
	
def printSetup(agent):
	s = "set palette model RGB functions 1-gray, 1-gray, 1-gray" + "\n"
	s = s + "set isosamples 100"
	return s
	
#this calculates the density function
def printCalc(agent, sigma_x, sigma_y, rho, target_x, target_y):
	s = "sigma_x = " + str(sigma_x) + "\n"
	s = s + "sigma_y = " + str(sigma_y) + "\n"
	s = s + "rho = " + str(rho) + "\n"
	s = s + "set pm3d at s explicit" + "\n"
		
	s = s + "splot 1.0/(2.0 * pi * "+str(sigma_x) +" * "+ str(sigma_y)+" * sqrt(1 - "+str(rho)+"**2)) \
		* exp(-1.0/2.0 * ((x - "+str(target_x)+")**2 / "+str(sigma_x)+"**2 + (y - "+str(target_y)+")**2/ "+str(sigma_y)+"**2 \
		- 2.0*"+str(rho)+"*x*y/("+str(sigma_x)+"*"+str(sigma_y)+"))) with pm3d"+ "\n"
	return s

#sigma_x and sigma_y are the std dev in either direction. rho is the correlation between x and y
def plot(agent, sigma_x, sigma_y, target_x, target_y):#, target_x, target_y):
	
	rho = 0	
	#since E = [[25 0],[0 25]] from the spec\
	f = open('plot.gpi', 'w')
	
	f.write(printHeader() + "\n")
	f.write(printSetup(agent) + "\n")
	f.write(printCalc(agent, sigma_x, sigma_y, rho, target_x, target_y) + "\n")
	f.write(printArrows(agent.x, agent.y, 5) + "\n")
	print "---------------plotting finished---------------\n\n"
	
'''
class Agent(object):
	"""Class handles all command and control logic for a teams tanks."""

	def __init__(self, x, y):
		self.x = x
		self.y = y


agent = Agent(20, 20);
covariance = np.matrix('50, 0, 0,   0,  0, 0;' +
						 '0, .1, 0,  0,  0, 0;' +
						 '0,  0, .1, 0,  0, 0;' +
						 '0,  0, 0,  50,  0, 0;' +
						 '0,  0, 0,  0, .1, 0;' +
						 '0,  0, 0,  0,  0, .1')

sigma_x = covariance.item((0, 0))
sigma_y = covariance.item((3, 3))
target_x = 100;
target_y = 100;
plot(agent,sigma_x, sigma_y, target_x, target_y);

'''
