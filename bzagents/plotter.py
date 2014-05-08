import pf_agent
	
	
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
	
	
	

	
	
	
	
def writePFtoFile(agent):
	print "---------------PF text File---------------\n"
	
	printHeader()
	printObstacles(agent)
	
	print "plot '-' with vectors head\n-381.65625 -381.65625 -4.6875 -4.6875\n-381.452830189 -349.66509434 -5.09433962264 -4.66981132075\n-381.233606557 -317.694672131 -5.53278688525 -4.6106557377\n"
	print "\ne"
	
	
	
	
	
	print "---------------end PF text File---------------\n\n"
	
	
