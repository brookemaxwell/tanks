import sys
import math
import time

from potential_field import Vector


def getCommandFromVectors(tank, curVector, desiredVector):
"""
y(t) = where I want to be at time t.
xt = where I am at time t.
(y(t) − xt) = error
P controller (P for proportional)
at = KP(y(t) − xt) + KD*d(y(t) - xt)/dt
		
	or in discrete land
		at = KP(y(t) − xt) + KD*d((y(t) − xt) − (y(t − 1) − xt − 1))/dt
"""
	return False #Vector
