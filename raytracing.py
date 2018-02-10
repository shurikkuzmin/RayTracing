# Working with arrays
import numpy
# Import pylab to paint
import pylab

nx = 200
ny = 200
scene = numpy.zeros((nx,ny,3))

#scene = numpy.array([[[0,0,1],[1,0,0]],[[0,1,0],[0,1,0]]])
#scene[1,1,:]=[200,0,200]
#print("Scene=", scene[0,:,2])

# Transformation of coordinates to the window
lx = 1
ly = 1
d = 1

def transform(px, py):
	x = (py - 0.5 * ny) / ny * lx
	y = (-px + 0.5 * nx) / nx * ly
	return [x,y,d]

def intersection(center,direction,tmin,tmax):
	direction 

#print(transform(0,0))	
#print(transform(nx,ny))
pylab.imshow(scene, interpolation='none')
pylab.show()