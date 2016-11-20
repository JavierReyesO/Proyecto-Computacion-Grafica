#!/usr/bin/python2.5 
import random 
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

#This function generates a 3D heightmap 
def fractal3D (_initial_range, passes, _roughness, size): 
        heightMap = [[255 for i in range (size)] for j in range (size)] #Create a new map, all points seeded to 255 (make this pretty much whatever you want) 
        randomRange = float (_initial_range) #Range to increase/decrease points by 
        roughness = float (2**(_roughness*-1)) #amount to reduce range by per iteration 
        sideLength = size - 1 
        while (sideLength >= 2): 
                halfSide = int (sideLength/2) 
                x = 0 
                #squaring step (using square-diamond algorithm) 
                for i in range (0, size-1, sideLength): 
                        for j in range (0, size-1, sideLength): 
                                avg = (heightMap[i][j]+ heightMap[i+sideLength][j]+heightMap[i][j+sideLength]+heightMap[i+sideLength][j+sideLength])/4.0 + random.randint (-1*int(randomRange), int(randomRange)) 
                                heightMap[i+halfSide][j+halfSide] = avg 
                #diamond step 
                for i in range (0, size, halfSide): 
                        for j in range ((i+halfSide)%sideLength, size, sideLength): 
                                avg  = (heightMap[(i-halfSide+size-1)%(size-1)][j]+heightMap[(i+halfSide)%(size-1)][j]+heightMap[i][(j+halfSide)%(size-1)]+heightMap[i][(j-halfSide+size-1)%(size-1)])/4.0 + random.randint (-1*int(randomRange), int(randomRange)) 
                                heightMap[i][j] = avg 
                sideLength = int (sideLength/2) 
                randomRange = randomRange*roughness #reduce range 
        return heightMap 

#These functions find the max/min of a 2D list. 
def min2D (list2D): 
        smallest = list2D[0][0] 
        for i in list2D: 
                for j in i: 
                        if (j < smallest): smallest = j 
        return smallest 

def max2D (list2D): 
        largest = list2D[0][0] 
        for i in list2D: 
                for j in i: 
                        if (j > largest): largest = j 
        return largest 

#this function takes a 3D heightmap and returns a 2D array of color data 
def buildColorMap3D(fractal): 
        minY = min2D(fractal)*-1 #this translates the array up, to remove negative values (no negative colors) 
        heightSpan = max2D(fractal)+minY #the difference between the highest and lowest point, used to compress large/small values to within the valid color spectrum 
        colorMap = [[0 for i in range(len(fractal[0]))] for j in range(len(fractal))] #initialized the color map 
        for i in range (len(colorMap)): 
                for j in range (len(colorMap)): 
                        blue = green = 0 #initialize blue & green to zero 
                        red = int((fractal[i][j]+minY)*767/heightSpan) #compresses height data to the valid color spectrum (256*256*256-1). NOT the full spectrum since you'll never have 0 red and blue/green >0 
                        if (red > 255): #color overflow spills into the next color 
                                blue = red-255 
                                red = 255 
                                if (blue > 255): 
                                        green = blue - 255 
                                        blue = 255 
                                        if (green > 255): 
                                                green = 255 #Didn't bother handling green overflow- it should never happen anyway. 
                        colorMap[i][j] = (red, green, blue) 
        return colorMap 

print "Generating fractal..."    
#heightMap = createVertexList (fractal3D (100, 0, 1.0, 129)) 
heightMap = buildColorMap3D(fractal3D(100, 0, 1.0, 513)) #build the map 
print "Done." 
window = glutCreateWindow("EntE")

# Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
# set the function pointer and invoke a function to actually register the callback, otherwise it
# would be very much like the C version of the code.    
glutDisplayFunc (DrawGLScene)

# Uncomment this line to get full screen.
#glutFullScreen()

# When we are doing nothing, redraw the scene.
glutIdleFunc(DrawGLScene)

# Register the function called when our window is resized.
glutReshapeFunc (ReSizeGLScene)

# Register the function called when the keyboard is pressed.  
glutKeyboardFunc (keyPressed)

# Initialize our window. 
InitGL(640, 480)

        
@win.event 
def on_draw(): 
        glClear(GL_COLOR_BUFFER_BIT) 
        glBegin (GL_POINTS) 
        #heightMap.draw (GL_POINTS) 
        #drawFractal2D(pointList, 0, 0, 1400.0, 480.0) 
        #drawFractal3D(heightMap, 0, 0, 0,0) 
        for i in range (len(heightMap)): #iterate over each pixel and draw it. 
                for j in range (len(heightMap)): 
                        glColor3ub (heightMap[i][j][0], heightMap[i][j][1], heightMap[i][j][2]) 
                        glVertex2i (i, j) 
                        #glVertex2i (4*i, 4*j) 
                        #glVertex2i (4*i-4, 4*j) 
                        #glVertex2i (4*i-4, 4*j-4) 
                        #glVertex2i (4*i, 4*j-4) 
        glEnd() 

pyglet.app.run() 