# Working with arrays
import numpy
# Import pylab to paint
import pylab


nx = 200
ny = 200
scene = numpy.zeros((nx,ny,3), dtype=int)

# Sphere specification
sphere = {}
sphere["center"] = numpy.array([0,-1,3])
sphere["radius"] = 1
sphere["color"] = numpy.array([10,0,0])

#sphere = {}
#sphere["center"] = numpy.array([+-2,0,4])
#sphere["radius"] = 1
#sphere["color"] = numpy.array([10,0,0])

# Transformation of coordinates to the window
lx = 1.0
ly = 1.0
d = 1.0

center = numpy.array([0,0,0])
def transform(px, py):

    x = (py - 0.5 * ny) / ny * lx
    y = (-px + 0.5 * nx) / nx * ly
    return numpy.array([x,y,d])

background_color = numpy.array([1,1,1])
def ray(center,direction,tmin,tmax):
    distance = center - sphere["center"]
    a = direction.dot(direction)
    b = 2 * numpy.dot(direction, distance)
    c = distance.dot(distance) - sphere["radius"]**2
    discriminant = b**2 - 4*a*c
    if discriminant > 0:
        t1 = (-b - numpy.sqrt(discriminant))/(2*a)
        t2 = (-b + numpy.sqrt(discriminant))/(2*a)
        if t1 > tmin and t1 < tmax:
            return sphere["color"]
        elif t2 > tmin and t2 < tmax:
            return sphere["color"]
    return background_color

for i in range(nx):
    for j in range(ny):
        direction = transform(i,j)
        scene[i,j,:] = ray(center, direction, 1.0, 10000.0)
#print(transform(0,0))  
#print(transform(nx,ny))
pylab.imshow(scene, interpolation='none')
pylab.show()