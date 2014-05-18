import pf_agent
from potential_field import PotentialField
from math import cos,sin,pi
	
	
#input vector has vector.magnitude and vector.magnitude	
def convertMagVectorToDirectionalVeclocityVector(vector):
	theta = vector.angle
	hypot = vector.magnitude
	
	if theta == float('Inf'):
		return [0,0]
	
	vy = sin(theta)* hypot
	
	vx = cos(theta)* hypot
	
	return [vx/50, vy/50]
		
	

def printHeader():
	print "# This part sets up the context\nset xrange [-400.0: 400.0]\nset yrange [-400.0: 400.0]\nunset key\nset size square\n"	
	
def printObstacles(agent):
	#an obstacle is as follows: [(100.0, 42.4264068712), (142.426406871, 0.0), (100.0, -42.4264068712), (57.5735931288, 5.19573633741e-15)]
	
	obstacles = agent.obstacles
	print "unset arrow"
	
	for ob in obstacles:
		for i in range(0,4):
			nextIndex = (i+1)%4
			print "set arrow from "+ str(ob[i][0])+", "+ str(ob[i][1]) + " to "+ str(ob[nextIndex][0])+", "+ str(ob[nextIndex][1]) + " nohead lt 3"
	
def printVectors(agent):
	print "\nplot '-' with vectors head"
	
	pf = PotentialField(agent)
	
	#pick the tank this represents
	
	#for tank in agent.mytanks:
		#print str(tank.x) + " "+ str(tank.y) +" " + str(tank.vx) +" " + str(tank.vy)
	
	tank = agent.mytanks[2]
	
	for x in range(-20,20):
		for y in range(-20,20):
			xCoor = x*20
			yCoor = y*20
							
			tank.x = xCoor
			tank.y = yCoor						
			vector = pf.get_desired_accel_vector(tank)
			dirVector = convertMagVectorToDirectionalVeclocityVector(vector)
			
			#should print like -381.65625 -381.65625 -4.6875 -4.6875
			print str(xCoor) + " "+ str(yCoor) +" " + str(dirVector[0]) +" " + str(dirVector[1])
			#print str(xCoor) + " "+ str(yCoor) +" " + str(1) +" " + str(1)
			#print str(vector.magnitude) +"    angle:" + str(vector.angle)
	print "e"		
	

def plot(agent):
	print "---------------PF text File---------------\n"
	
	printHeader()
	printObstacles(agent)
	printVectors(agent)
	
	#print "plot '-' with vectors head\n-381.65625 -381.65625 -4.6875 -4.6875\n-381.452830189 -349.66509434 -5.09433962264 -4.66981132075\n-381.233606557 -317.694672131 -5.53278688525 -4.6106557377\n"
	
	
	
	
	
	print "---------------end PF text File---------------\n\n"
	
	
