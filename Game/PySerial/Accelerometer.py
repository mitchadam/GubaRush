

""" Orientation:
up -- Positive Y
down --  negative Y
left body -- Positive X
right body -- Negative X
into body -- Positive Z
out of body -- Negative Z """
prevX, prevY, prevZ = 0, 0, 0
preMov = [0,0]


def readAccel(AcX, AcY, AcZ):
	# movement[vertical, horizontal]
	# 1 represents up and right 
	# -1 represents down and left
	movement = [0,0]

	# see if acceleration has changed and passes a certain threshold
	# usual acclerometer data varies by maximum 500
	# a large change of movement would vary by a large amount according to the MPU sensitivty

	# a jump represents a large change in positive Y direction
	if (AcY - preY >= 5000):
		if (preMov[0] == -1):
			movement = 0
		else:
			movement = 1
	
	# a duck represents a large change in negative Y direction
	
	if (AcY - preY <= -1000):
		if()
		movement[0] = 1

	# a left movement represents a large change in 
	

