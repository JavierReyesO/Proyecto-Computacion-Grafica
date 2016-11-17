#!/usr/bin/env python

#
# This code was created by Richard Campbell '99 (ported to Python/PyOpenGL by John Ferguson 2000)
#
# The port was based on the PyOpenGL tutorial module: dots.py  
#
# If you've found this code useful, please let me know (email John Ferguson at hakuin@voicenet.com).
#
# See original source and C based tutorial at http://nehe.gamedev.net
#
# Note:
# -----
# This code is not a good example of Python and using OO techniques.  It is a simple and direct
# exposition of how to use the Open GL API in Python via the PyOpenGL package.  It also uses GLUT,
# which in my opinion is a high quality library in that it makes my work simpler.  Due to using
# these APIs, this code is more like a C program using function based programming (which Python
# is in fact based upon, note the use of closures and lambda) than a "good" OO program.
#
# To run this code get and install OpenGL, GLUT, PyOpenGL (see http://www.python.org), and PyNumeric.
# Installing PyNumeric means having a C compiler that is configured properly, or so I found.  For 
# Win32 this assumes VC++, I poked through the setup.py for Numeric, and chased through disutils code
# and noticed what seemed to be hard coded preferences for VC++ in the case of a Win32 OS.  However,
# I am new to Python and know little about disutils, so I may just be not using it right.
#
# BTW, since this is Python make sure you use tabs or spaces to indent, I had numerous problems since I 
# was using editors that were not sensitive to Python.
#
# Modified on May 2nd,2004 by Travis Wells to fix some GLUT issues and missing import
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import numpy
import ast
# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = '\033'
LEFT		= '\037'
UP 			= '\038'
RIGHT 	= '\039'
DOWN 		= '\040'

# Number of the glut window.
window = 0


vertices = {}
vertices['a'] = [-1.0, 1.0, 0.0]
vertices['b'] = [1.0, 1.0, 0.0]
vertices['c'] = [-1.0, -1.0, 0.0]
vertices['d'] = [1.0, -1.0, 0.0]
vertices['e'] = [-1.0, 1.0, 0.0]
vertices['f'] = [1.0, 1.0, 0.0]
vertices['g'] = [-1.0, -1.0, 0.0]
vertices['h'] = [1.0, -1.0, 0.0]
vNames = ['a','b','c','d','e','f','g','h']
currentV = 0
currentM = 1

vertices2 = {}
vertices2['a'] = [-1.0, 1.0, 0.0]
vertices2['b'] = [1.0, 1.0, 0.0]
vertices2['c'] = [-1.0, -1.0, 0.0]
vertices2['d'] = [1.0, -1.0, 0.0]
vertices2['e'] = [-1.0, 1.0, 0.0]
vertices2['f'] = [1.0, 1.0, 0.0]
vertices2['g'] = [-1.0, -1.0, 0.0]
vertices2['h'] = [1.0, -1.0, 0.0]

for i in vNames:
	vertices2[i][1]+=2.5
	vertices2[i][2]+=0.01

vertices_actual = vertices


# A general OpenGL initialization function.  Sets all of the initial parameters. 
def InitGL(Width, Height):				# We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)	# This Will Clear The Background Color To Black
    glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
    glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading
	
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()					# Reset The Projection Matrix
										# Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)

# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:						# Prevent A Divide By Zero If The Window Is Too Small 
	    Height = 1

    glViewport(0, 0, Width, Height)		# Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)



# The main drawing function. 
def DrawGLScene():
	global vertices, vNames, currentV, currentTime, vertices2

	# Clear The Screen And The Depth Buffer
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()					# Reset The View 

	#Move into the screen 6.0 units.
	glTranslatef(0.0, 0.0, -6.0)

	# TOP
	glBegin(GL_QUADS)                   # Start drawing a 4 sided polygon
	glColor3f(0.0,1.0,0.0)			# Set The Color To Green
	glVertex3f(vertices['a'][0],vertices['a'][1],vertices['a'][2])
	glVertex3f(vertices['b'][0],vertices['b'][1],vertices['b'][2])
	glVertex3f(vertices['f'][0],vertices['f'][1],vertices['f'][2])
	glVertex3f(vertices['e'][0],vertices['e'][1],vertices['e'][2])
	glEnd()


	# Move Left 3.0 units and 
	#glTranslatef(-3.0, 0.0, 0.0)

	# FRONT
	glBegin(GL_QUADS)                   # Start drawing a 4 sided polygon
	glColor3f(1.0,0.0,0.0)			# Set The Color To Red
	glVertex3f(vertices['a'][0],vertices['a'][1],vertices['a'][2])
	glVertex3f(vertices['b'][0],vertices['b'][1],vertices['b'][2])
	glVertex3f(vertices['d'][0],vertices['d'][1],vertices['d'][2])
	glVertex3f(vertices['c'][0],vertices['c'][1],vertices['c'][2])
	glEnd()                             # We are done with the polygon                           # We are done with the polygon

	# Move Right 3.0 units.
	#glTranslatef(6.0, 0.0, 0.0)

	# LEFT face
	glBegin(GL_QUADS)                   # Start drawing a 4 sided polygon
	glColor3f(0.0,0.0,1.0)			# Set The Color To Blue
	glVertex3f(vertices['a'][0],vertices['a'][1],vertices['a'][2])
	glVertex3f(vertices['e'][0],vertices['e'][1],vertices['e'][2])
	glVertex3f(vertices['g'][0],vertices['g'][1],vertices['g'][2])
	glVertex3f(vertices['c'][0],vertices['c'][1],vertices['c'][2])
	glEnd()                             # We are done with the polygon


	#SEGUNDO CUBO

	# TOP
	glBegin(GL_QUADS)                   # Start drawing a 4 sided polygon
	glColor3f(0.0,1.0,0.0)			# Set The Color To Green
	glVertex3f(vertices2['a'][0],vertices2['a'][1],vertices2['a'][2])
	glVertex3f(vertices2['b'][0],vertices2['b'][1],vertices2['b'][2])
	glVertex3f(vertices2['f'][0],vertices2['f'][1],vertices2['f'][2])
	glVertex3f(vertices2['e'][0],vertices2['e'][1],vertices2['e'][2])
	glEnd()


	# Move Left 3.0 units and 
	#glTranslatef(-3.0, 0.0, 0.0)

	# FRONT
	glBegin(GL_QUADS)                   # Start drawing a 4 sided polygon
	glColor3f(1.0,0.0,0.0)			# Set The Color To Red
	glVertex3f(vertices2['a'][0],vertices2['a'][1],vertices2['a'][2])
	glVertex3f(vertices2['b'][0],vertices2['b'][1],vertices2['b'][2])
	glVertex3f(vertices2['d'][0],vertices2['d'][1],vertices2['d'][2])
	glVertex3f(vertices2['c'][0],vertices2['c'][1],vertices2['c'][2])
	glEnd()                             # We are done with the polygon                           # We are done with the polygon

	# Move Right 3.0 units.
	#glTranslatef(6.0, 0.0, 0.0)

	# LEFT face
	glBegin(GL_QUADS)                   # Start drawing a 4 sided polygon
	glColor3f(0.0,0.0,1.0)			# Set The Color To Blue
	glVertex3f(vertices2['a'][0],vertices2['a'][1],vertices2['a'][2])
	glVertex3f(vertices2['e'][0],vertices2['e'][1],vertices2['e'][2])
	glVertex3f(vertices2['g'][0],vertices2['g'][1],vertices2['g'][2])
	glVertex3f(vertices2['c'][0],vertices2['c'][1],vertices2['c'][2])
	glEnd() 

	#  since this is double buffered, swap the buffers to display what just got drawn. 
	glutSwapBuffers()



# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)  
def keyPressed(*args):
	global vertices, vNames, currentV, rquadSum, vertices_actual, currentM, vertices2
	# If escape is pressed, kill everything.
	if args[0] == ESCAPE:
		glutDestroyWindow(window)
		sys.exit()

	# X axis
	elif args[0] == 'a':
		vertices_actual[vNames[currentV]][0]-=0.1
	elif args[0] == 'd':
		vertices_actual[vNames[currentV]][0]+=0.1
		
	# Y axis
	elif args[0] == 's':
		vertices_actual[vNames[currentV]][1]-=0.1
	elif args[0] == 'w':
		vertices_actual[vNames[currentV]][1]+=0.1

	# Z axis
	elif args[0] == 'e':
		vertices_actual[vNames[currentV]][2]-=0.1
	elif args[0] == 'q':
		vertices_actual[vNames[currentV]][2]+=0.1

	# change vertix
	elif args[0] == 'p':
		currentV = (currentV+1)%8

	elif args[0] == 'o':
		if currentM == 1: 
			vertices_actual = vertices2
			currentM = 2
			currentV = 0
		else:
			vertices_actual = vertices
			currentM = 1
			currentV = 0


	elif args[0] == 'g':
		f=file("cubo1.txt","w");
		for k in vertices:
			f.write(k+"@"+str(vertices[k])+"\n")
		f.close()

	elif args[0] == 'b':
		f=file("cubo2.txt","w");
		for k in vertices2:
			f.write(k+"@"+str(vertices2[k])+"\n")
		f.close()	

	elif args[0] == 'h':
		lines = [line.rstrip('\n') for line in open('cubo1.txt')]
		aux_vert = {}
		for i in lines:
			k,lista = i.split("@")
			final = map(float, lista[1:-2].split(','))
			aux_vert[k] = final
	
		vertices = aux_vert
		currentV = 0
	
	elif args[0] == 'n':
		lines2 = [line.rstrip('\n') for line in open('cubo2.txt')]
		aux_vert2 = {}
		for i2 in lines2:
			k2,lista2 = i2.split("@")
			final2 = map(float, lista2[1:-2].split(','))
			aux_vert2[k2] = final2
	
		vertices2 = aux_vert2
		currentV = 0
			

def main():
	global window
	# For now we just pass glutInit one empty argument. I wasn't sure what should or could be passed in (tuple, list, ...)
	# Once I find out the right stuff based on reading the PyOpenGL source, I'll address this.
	glutInit(())

	# Select type of Display mode:   
	#  Double buffer 
	#  RGBA color
	# Alpha components supported 
	# Depth buffer
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
	
	# get a 640 x 480 window 
	glutInitWindowSize(640, 480)
	
	# the window starts at the upper left corner of the screen 
	glutInitWindowPosition(0, 0)
	
	# Okay, like the C version we retain the window id to use when closing, but for those of you new
	# to Python (like myself), remember this assignment would make the variable local and not global
	# if it weren't for the global declaration at the start of main.
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


# Print message to console, and kick off the main to get it rolling.
print "Hit ESC key to quit."
if __name__ == '__main__':
	try:
		GLU_VERSION_1_2
	except:
		print "Need GLU 1.2 to run this demo"
		sys.exit(1)
	main()
	glutMainLoop()
