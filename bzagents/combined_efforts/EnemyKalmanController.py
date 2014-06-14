from geometry import Vector
from math import atan2, pi
from bzrc import Command
from numpy import matrix


"""A controller for a single target. This implements the Kalman filter stuff"""
class TankController(object):
	
	def __init__(self, tank, timeInterval):
		self.prev_speed_error = 0
		self.prev_angle_error = 0
		self.tank = tank
		self.lastX = tank.x
		self.lastY = tank.y
		self.lastVX = 0
		self.lastVY = 0
		self.deltaTime = timeInterval
		
		#this matrix contains the original tank state of the location,speed, and acc of the enenmy tank. It is a column vector.
		self.mewt = matrix( "200; 0; 0; 0; 0; 0" )
		#print str(self.mewt) +"\n\n"
		#covariance matrix 
		self.Et = matrix('20, 0, 0,   0,  0, 0;' +
						 '0, .1, 0,  0,  0, 0;' +
						 '0,  0, .1, 0,  0, 0;' +
						 '0,  0, 0,  20,  0, 0;' +
						 '0,  0, 0,  0, .1, 0;' +
						 '0,  0, 0,  0,  0, .1')
		
		
		#matric which need to be intialized only once
		self.F = matrix( '1,  4, 2,  0,  0, 0;' +
						 '0,  1, 4,  0,  0, 0;' +
						 '0,  0, 1,  0,  0, 0;' +
						 '0,  0, 0,  1,  4, 2;' +
						 '0,  0, 0,  0,  1, 4;' +
						 '0,  0, 0,  0,  0, 1')
		'''
		self.Ex = matrix('25, 0, 0,   0,  0, 0;' +
						 '0,  5, 0,   0,  0, 0;' +
						 '0,  0, .1, 0,  0, 0;' +
						 '0,  0, 0,  25,  0, 0;' +
						 '0,  0, 0,   0, 5, 0;' +
						 '0,  0, 0,   0,  0, .1')
		'''				 
		self.Ex = matrix('.1, 0, 0,   0,  0, 0;' +
						 '0,  .1, 0,   0,  0, 0;' +
						 '0,  0, 50, 0,  0, 0;' +
						 '0,  0, 0,  .1,  0, 0;' +
						 '0,  0, 0,   0, .1, 0;' +
						 '0,  0, 0,   0,  0, 50')
		
		self.H = matrix('1 0 0 0 0 0;'+
						'0 0 0 1 0 0')		
		
		self.Ez = matrix('25, 0; 0, 25')
		
		self.I =  matrix('1, 0, 0, 0, 0, 0;' +
						 '0, 1, 0, 0, 0, 0;' +
						 '0, 0, 1, 0, 0, 0;' +
						 '0, 0, 0, 1, 0, 0;' +
						 '0, 0, 0, 0, 1, 0;' +
						 '0, 0, 0, 0, 0, 1')

		
	"""Update the position of the tank based off the given sensor reading"""
	def updateTarget(self, targetTank):
		# the following few lines help us avoid seeing "self" everywhere and hopefully avoids errors
		mewt = self.mewt
		Et = self.Et
		F = self.F 
		Ex = self.Ex 
		H = self.H	
		Ez = self.Ez
		I = self.I
		ztplus1 = self.makeMatrixFromObserved(targetTank)
	
		#print "enemy position reading: ("+ str(targetTank.x)+", "+str(targetTank.y)+")"
		#print "in filter " + str(mewt[0][0])+", "+str(mewt[3][0])+") " 
		#print "enemy velocity.  vx: "+ str(self.lastVX) + "   vy: "+ str(self.lastVY)
		
		
		FEtFtranPlusEx = ( F * Et * (F.T) ) + Ex
		KalmanGain = FEtFtranPlusEx * H.T * ((H* FEtFtranPlusEx*H.T +Ez).I)


	
		mewtplus1 = (F*mewt)+ (KalmanGain*(ztplus1 - (H*F*mewt)))
		Etplus1 = (I - (KalmanGain*H))* FEtFtranPlusEx
		
		self.mewt = mewtplus1
		self.Et = Etplus1
		
		#print "new mewt "+ str(mewt)
		
	
	
	"""Using the last X and Y position and velocity, predict the next X,Y coordiante for the enemy tank  """
	def getTargetPosAtNextInterval(self):
		predictionMatrix = self.F * self.mewt
		#print "We predict the tank will be at ("+ str(predictionMatrix[0,0]) +", "+ str(predictionMatrix[3,0])+")"+"\n\n\n"
		return predictionMatrix[0,0], predictionMatrix[3,0]
		
	def makeMatrixFromObserved(self, targetTank):
		
		timeDiff = self.deltaTime
		x = targetTank.x
		y = targetTank.y
		if(targetTank.status == "dead"):
			#print "dead " + str(targetTank.x) + ", " + str(targetTank.y)
			x = 200
			y = 0
		vx = (x - self.lastX)/timeDiff
		vy = (y - self.lastY)/timeDiff
		ax = (vx - self.lastVX)/timeDiff
		ay = (vy - self.lastVY)/timeDiff
			
		observationMatrix = matrix( str(x) +'; '+ str(y))
		
		self.lastX = x
		self.lastY = y
		self.lastVX = vx
		self.lastVY = vy
		
		return observationMatrix
		
	def isAlive(self):
		return 1500 > lastX or lastX > -1500
		
