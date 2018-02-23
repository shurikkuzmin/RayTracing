# Working with arrays
import numpy
# Import pylab to paint
import pylab


nx = 200
ny = 200
scene = numpy.zeros((nx,ny,3), dtype=numpy.uint8)

# Spheres specification
spheres = [{},{},{},{}]

spheres[0]["center"] = numpy.array([0,-1,3])
spheres[0]["radius"] = 1
spheres[0]["color"] = numpy.array([255,0,0], dtype=numpy.uint8)

spheres[1]["center"] = numpy.array([2,0,4])
spheres[1]["radius"] = 1
spheres[1]["color"] = numpy.array([0,255,0])

spheres[2]["center"] = numpy.array([-2,0,4])
spheres[2]["radius"] = 1
spheres[2]["color"] = numpy.array([0,0,255])

spheres[3]["center"] = numpy.array([0,-5001,0])
spheres[3]["radius"] = 5000
spheres[3]["color"] = numpy.array([255,255,0])

# Specification of lights
lights = [{},{},{}]

lights[0]["type"] = "ambient"
lights[0]["intensity"] = 0.2

lights[1]["type"] = "point" 
lights[1]["intensity"] = 0.6
lights[1]["position"] = numpy.array([2, 1, 0])

lights[2]["type"] = "directional"
lights[2]["intensity"] = 0.2
lights[2]["direction"] = numpy.array([1, 4, 4])

# Transformation of coordinates to the window
lx = 1.0
ly = 1.0
d = 1.0

# Coordinates of an eye
center = numpy.array([0,0,0])

def transform(px, py):

    x = (py - 0.5 * ny) / ny * lx
    y = (-px + 0.5 * nx) / nx * ly
    return numpy.array([x,y,d])

background_color = numpy.array([255,255,255],dtype = numpy.uint8)
def ray(center,direction,tmin,tmax):
    indclosest = -1
    tclosest = tmax
    for ind, sphere in enumerate(spheres):
        distance = center - sphere["center"]
        a = direction.dot(direction)
        b = 2 * numpy.dot(direction, distance)
        c = distance.dot(distance) - sphere["radius"]**2
        discriminant = b**2 - 4*a*c
        if discriminant > 0:
            t1 = (-b - numpy.sqrt(discriminant))/(2*a)
            t2 = (-b + numpy.sqrt(discriminant))/(2*a)
            if t1 > tmin and t1 < tmax and t1 < tclosest:
                tclosest = t1
                indclosest = ind
            elif t2 > tmin and t2 < tmax and t2 < tclosest:
                tclosest = t2
                indclosest = ind

    if indclosest != -1:       
        return spheres[indclosest]["color"]
    else:
        return background_color

for i in range(nx):
   for j in range(ny):
       direction = transform(i,j)
       scene[i,j,:] = ray(center, direction, 1.0, 10000.0)

pylab.imshow(scene, interpolation='none')
pylab.show()