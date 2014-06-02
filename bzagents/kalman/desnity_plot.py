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
	
#this sets the range of the density function. right now it doesn't actually do more than the demo
def printArrows(agent):
	print "unset arrow"
	print "set arrow from 0, 0 to -150, 0 nohead front lt 3"
	print "set arrow from -150, 0 to -150, -50 nohead front lt 3"
	print "set arrow from -150, -50 to 0, -50 nohead front lt 3"
	print "set arrow from 0, -50 to 0, 0 nohead front lt 3"
	print "set arrow from 200, 100 to 200, 330 nohead front lt 3"
	print "set arrow from 200, 330 to 300, 330 nohead front lt 3"
	print "set arrow from 300, 330 to 300, 100 nohead front lt 3"
	print "set arrow from 300, 100 to 200, 100 nohead front lt 3"
	
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
		- 2.0*"+str(rho)+"*x*y/("+str(sigma_x)+"*"+str(sigma_y))))+" with pm3d"
	

#sigma_x and sigma_y are the std dev in either direction. rho is the correlation between x and y
def plot(agent):
	print "---------------PF text File---------------\n"
	
	sigma_x = 5
	sigma_y = 5
	rho = 0
	
	#since E = [[25 0],[0 25]] from the spec
	
	printHeader()
	printArrows(agent)
	printSetup(agent)
	printCalc(agent, sigma_x, sigma_y, rho)

	print "---------------end PF text File---------------\n\n"
