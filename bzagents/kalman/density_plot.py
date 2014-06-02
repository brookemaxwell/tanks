#!/usr/bin/python -tt

# Create Multivariate density plot

from __future__ import division

import geometry
import numpy

from math import cos,sin,pi	

def printHeader():
	print "# This part sets up the context"
	print "set xrange [-400.0: 400.0]"
	print "set yrange [-400.0: 400.0]"
	print "set pm3d"
	print "set view map"
	print "unset key"
	print "set size square"
	
#this sets the range of the density function (?). right now it doesn't actually do more than the demo
def printArrows(x, y, radius):
	print "unset arrow"
	print "set arrow from "+str(x - radius) + ", "+str(y - radius)+" to "+str(x - radius) + ", "+str(y + radius) +" nohead front lt 3"
	print "set arrow from "+str(x - radius) + ", "+str(y - radius)+" to "+str(x + radius) + ", "+str(y - radius) +" nohead front lt 3"
	print "set arrow from "+str(x - radius) + ", "+str(y + radius)+" to "+str(x + radius) + ", "+str(y + radius) +" nohead front lt 3"
	print "set arrow from "+str(x + radius) + ", "+str(y - radius)+" to "+str(x + radius) + ", "+str(y + radius) +" nohead front lt 3"
	
def printSetup(agent):
	print "set palette model RGB functions 1-gray, 1-gray, 1-gray"
	print "set isosamples 100"
	
#this calculates the density function
def printCalc(agent, sigma_x, sigma_y, rho):
	print "sigma_x = " + str(sigma_x)
	print "sigma_y = " + str(sigma_y)
	print "rho = " + str(rho)
	print "splot 1.0/(2.0 * pi * "+str(sigma_x) +" * "+ str(sigma_y)+" * sqrt(1 - "+str(rho)+"**2)) \
		* exp(-1.0/2.0 * (x**2 / "+str(sigma_x)+"**2 + y**2 / "+str(sigma_y)+"**2 \
		- 2.0*"+str(rho)+"*x*y/("+str(sigma_x)+"*"+str(sigma_y)+"))) with pm3d"

#sigma_x and sigma_y are the std dev in either direction. rho is the correlation between x and y
def plot(agent, target_x, target_y):
	print "---------------PF text File---------------\n"
	
	sigma_x = 5
	sigma_y = 5
	rho = 0	
	#since E = [[25 0],[0 25]] from the spec
	
	printHeader()
	printArrows(agent.x, agent.y, 5)
	printArrows(target_x, target_y, 5)
	printSetup(agent)
	printCalc(agent, sigma_x, sigma_y, rho)

	print "---------------end PF text File---------------\n\n"
