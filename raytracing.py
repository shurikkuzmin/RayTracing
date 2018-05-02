# Working with arrays
import numpy
# Import pylab to paint
import pylab


nx = 300
ny = 300
scene = numpy.zeros((nx,ny,3), dtype=numpy.uint8)

# Spheres specification
spheres = [{},{},{},{}]
#spheres[0]["center"] = numpy.array([0,0,3])
#spheres[0]["radius"] = 1
#spheres[0]["color"] = numpy.array([255,0,0], dtype=numpy.uint8)
#spheres[0]["specular"] = 100
#spheres[0]["reflective"] = 0.1
#spheres[0]["transmissive"] = 0.8
#spheres[0]["refraction"] = 1.2

#spheres[1]["center"] = numpy.array([0,-5001,0])
#spheres[1]["radius"] = 5000
#spheres[1]["color"] = numpy.array([255,255,0])
#spheres[1]["specular"] = 1000
#spheres[1]["reflective"] = 0.1
#spheres[1]["transmissive"] = 0.0
#spheres[1]["refraction"] = 1.2

spheres[0]["center"] = numpy.array([0,-1,3])
spheres[0]["radius"] = 1
spheres[0]["color"] = numpy.array([255,0,0], dtype=numpy.uint8)
spheres[0]["specular"] = 100
spheres[0]["reflective"] = 0.1
spheres[0]["transmissive"] = 0.8
spheres[0]["refraction"] = 1.2

spheres[1]["center"] = numpy.array([2,0,4])
spheres[1]["radius"] = 1
spheres[1]["color"] = numpy.array([0,255,0])
spheres[1]["specular"] = 500
spheres[1]["reflective"] = 0.3
spheres[1]["transmissive"] = 0.4
spheres[1]["refraction"] = 1.2

spheres[2]["center"] = numpy.array([-2,0,4])
spheres[2]["radius"] = 1
spheres[2]["color"] = numpy.array([0,0,255])
spheres[2]["specular"] = 10
spheres[2]["reflective"] = 0.4
spheres[2]["transmissive"] = 0.5
spheres[2]["refraction"] = 1.2

spheres[3]["center"] = numpy.array([0,-5001,0])
spheres[3]["radius"] = 5000
spheres[3]["color"] = numpy.array([255,255,0])
spheres[3]["specular"] = 1000
spheres[3]["reflective"] = 0.0
spheres[3]["transmissive"] = 0.0
spheres[3]["refraction"] = 1.2

# Specification of lights
#lights = [{},{},{}]
lights = [{}, {}]

lights[0]["type"] = "ambient"
lights[0]["intensity"] = 0.2

lights[1]["type"] = "point" 
lights[1]["intensity"] = 0.6
lights[1]["position"] = numpy.array([2, 1, 0])

#lights[2]["type"] = "directional"
#lights[2]["intensity"] = 0.2       
#lights[2]["direction"] = numpy.array([1, 4, 4])

# Transformation of coordinates to the window
lx = 1.0
ly = 1.0
d = 1.0

# Translation of the eye and the window
shift_x = 0.0
shift_y = 0.0
shift_z = 0.0

# Coordinates of an eye
eye = numpy.array([shift_x,shift_y,shift_z])

# Angle of camera rotation in XZ plane
rotation = 0.0 * numpy.pi / 180.0

# Recursion depth
recursion_depth = 3

# Background color
background_color = numpy.array([0,0,0],dtype = numpy.uint8)

def transform(px, py):
    x = (py - 0.5 * ny) / ny * lx
    y = (-px + 0.5 * nx) / nx * ly
    return numpy.array([x+shift_x,y+shift_y,d+shift_z])


# Calculate ray and the color it hits
def ray(eye, direction, tmin, tmax, depth):

    indclosest, tclosest = closestIntersection(eye, direction, tmin, tmax)
    if indclosest != -1:
        sphere = spheres[indclosest]  
        intersection = eye + tclosest * direction     
        normal = (intersection - sphere["center"]) / sphere["radius"]
        specularity = sphere["specular"]
        reflectivity = sphere["reflective"]
        transmissivity = sphere["transmissive"]
        refraction = sphere["refraction"]

        #local_color = numpy.array(sphere["color"], dtype = numpy.uint8)
        local_color = numpy.array(sphere["color"] * computeLight(eye, intersection, normal, specularity), dtype = numpy.uint8)
        if depth <= 0:
            return local_color
        else:
            dir_normal = normal * numpy.dot(direction, normal)
            dir_tau = direction - normal * numpy.dot(direction, normal)
            dir_abs = numpy.sqrt(numpy.dot(direction, direction))

            reflected_color = numpy.array([0,0,0], dtype=numpy.uint8)
            transmissed_color = numpy.array([0,0,0], dtype=numpy.uint8)
            
            if reflectivity > 0:
                reflected_direction = dir_tau - dir_normal
                reflected_color = ray(intersection, reflected_direction, 0.0001, tmax, depth - 1)
            
            if transmissivity > 0:
                if numpy.dot(dir_normal, normal) < 0:
                    # Going into inside sphere
                    transmissed_direction = dir_normal + dir_tau / refraction
                    transmissed_color = ray(intersection, transmissed_direction, 0.0001, tmax, depth - 1)
                else:
                    # Going out
                    #if numpy.sqrt(1.0-(numpy.dot(direction, normal)/dir_abs)**2)*refraction < 1.0:
                    transmissed_direction = dir_normal + dir_tau * refraction
                    transmissed_color = ray(intersection, transmissed_direction, 0.0001, tmax, depth - 1)
            return local_color * (1 - reflectivity - transmissivity) + reflectivity * reflected_color + transmissivity * transmissed_color
    return background_color

def closestIntersection(point, direction, tmin, tmax):
    indclosest = -1
    tclosest = tmax
    for ind, sphere in enumerate(spheres):
        distance = point - sphere["center"]
        a = numpy.dot(direction, direction)
        b = 2 * numpy.dot(direction, distance)
        c = numpy.dot(distance, distance) - sphere["radius"]*sphere["radius"]
        discriminant = b*b - 4*a*c
        if discriminant > 0:
            t1 = (-b - numpy.sqrt(discriminant))/(2*a)
            t2 = (-b + numpy.sqrt(discriminant))/(2*a)
            if t1 > tmin and t1 < tmax and t1 < tclosest:
                tclosest = t1
                indclosest = ind
            elif t2 > tmin and t2 < tmax and t2 < tclosest:
                tclosest = t2
                indclosest = ind
    return indclosest, tclosest

def computeLight(eye, intersection, normal, specularity):
    intensity = 0
    for light in lights:
        if light["type"] == "ambient":
            intensity = intensity + light["intensity"]
        elif light["type"] == "point" or light["type"] == "directional":
            if light["type"] == "point":
                direction = light["position"] - intersection
                tmax = 1.0
            else:
                direction = light["direction"]
                tmax = 10000.0

            ind, t = closestIntersection(intersection, direction, 0.0001, tmax)
            if ind != -1:
                continue

            norm = numpy.sqrt(numpy.dot(direction, direction))
            if norm > 1e-6:
                direction = direction / norm

            cos = numpy.dot(direction, normal)
            if cos > 0:
                intensity = intensity + light["intensity"] * cos

                # Check the specular reflection
                reflection = 2*normal*cos - direction
                intersection2 = eye - intersection
                norm = numpy.sqrt(numpy.dot(intersection2, intersection2))
                if norm > 1e-6:
                    intersection2 = intersection2/norm
                cos2 = numpy.dot(intersection2, reflection)
                if cos2 > 0 and specularity > 0:
                    intensity = intensity + light["intensity"] * (cos2**specularity) 
    if intensity > 1.0:
        intensity = 1.0
    return intensity 

for i in range(nx):
   for j in range(ny):
       direction = transform(i,j) - eye
       direction2 = direction

       direction2[0] = direction[0] * numpy.cos(rotation) - direction[2] * numpy.sin(rotation)
       direction2[1] = direction[1]
       direction2[2] = direction[0] * numpy.sin(rotation) + direction[2] * numpy.cos(rotation)

       scene[i,j,:] = ray(eye, direction2, 1.0, 10000.0, recursion_depth)

pylab.imshow(scene)
pylab.show()