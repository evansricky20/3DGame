import random

import pygame
import time
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

sphereList = []

class Sphere:
   def __init__(self, name, radius, x_cord, y_cord, z_cord):
      self.name = name
      self.radius = radius
      self.x_cord = x_cord
      self.y_cord = y_cord
      self.z_cord = z_cord
      sphereList.append(self)
      self.red = random.uniform(0, 1)
      self.green = random.uniform(0, 1)
      self.blue = random.uniform(0, 1)

   def draw(self):
      glColor3f(self.red, self.green, self.blue)
      glPushMatrix()
      glTranslatef(self.x_cord, self.y_cord, self.z_cord)
      sphere = gluNewQuadric()
      gluSphere(sphere, self.radius, 32, 32)
      glPopMatrix()


   def move(self, leftFlag, rightFlag, upFlag, downFlag, spaceFlag, ctrlFlag):
      if leftFlag == 1:  # if left key bind is active, then subtract from characters x coordiante to move left
         self.x_cord = self.x_cord - 0.05
      if rightFlag == 1:  # Opposite if moving right
         self.x_cord = self.x_cord + 0.05
      if upFlag == 1:
         self.z_cord = self.z_cord - 0.05
      if downFlag == 1:
         self.z_cord = self.z_cord + 0.05
      if spaceFlag == 1:
         self.y_cord = self.y_cord + 0.05
      if ctrlFlag == 1:
         self.y_cord = self.y_cord - 0.05


def createPlanet():
   planet = Sphere(f"planet_{random.randint}", 1, 0, 0, 0)



# Main
#
# Create opengl renderings
def main():
   pygame.init()
   display = (1000,600)
   pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

   gluPerspective(90, (display[0]/display[1]), 0.1, 50.0)
   gluLookAt(0.0, 5.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

   # Flags to get status of bob
   upFlag = 0
   downFlag = 0
   leftFlag = 0
   rightFlag  = 0
   spaceFlag = 0
   ctrlFlag = 0
   activePlanetIndex = 0

   ball = Sphere("ball1", 1, 2, 2, 0)
   ball2 = Sphere("ball2", 2, 1, 1, 0)

   activePlanet = sphereList[activePlanetIndex]
   #print(sphereList[0].name)

   while True:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
            quit()

         # Using pygame keys to find keys being pressed
         # If specified key is pressed, its flag is set
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
               #print("Left pressed")
               leftFlag = 1
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
               #print("Right pressed")
               rightFlag = 1
            if event.key == pygame.K_UP or event.key == pygame.K_w:
               #print("Up pressed")
               upFlag = 1
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
               #print("Down pressed")
               downFlag = 1
            if event.key == pygame.K_SPACE:
               #print("Space pressed")
               spaceFlag = 1
            if event.key == pygame.K_LCTRL:
               #print("CTRL pressed")
               ctrlFlag  = 1
            if event.key == pygame.K_COMMA:
               print("Prev pressed")
               if activePlanetIndex == 0:
                  print("Current index 0, cannot go out of range.")
               else:
                  activePlanetIndex = activePlanetIndex - 1
                  activePlanet = sphereList[activePlanetIndex]
               print(activePlanet.name)
            if event.key == pygame.K_PERIOD:
               print("Next pressed")
               if activePlanetIndex == len(sphereList)-1:
                  print(f"Current index is {activePlanetIndex}, cannot go out of range.")
               else:
                  activePlanetIndex = activePlanetIndex + 1
                  activePlanet = sphereList[activePlanetIndex]
               print(activePlanet.name)


         # Using pygame keys to find keys released after being pressed
         # If specified key is released its flag is reset
         if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
               #print("Left released")
               leftFlag = 0
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
               #print("Right released")
               rightFlag = 0
            if event.key == pygame.K_UP or event.key == pygame.K_w:
               #print("Up released")
               upFlag = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
               #print("Down released")
               downFlag = 0
            if event.key == pygame.K_SPACE:
               #print("Space released")
               spaceFlag = 0
            if event.key == pygame.K_LCTRL:
               #print("CTRL released")
               ctrlFlag  = 0

      #ball.move(leftFlag, rightFlag, upFlag, downFlag, spaceFlag)
      for i in sphereList:
         if i.name == activePlanet.name:
            i.move(leftFlag, rightFlag, upFlag, downFlag, spaceFlag, ctrlFlag)

      #time = pygame.time.get_ticks()/1000 # returns time in miliseconds / 1000 to get seconds
      #print(time)
      #sinTest = np.sin(time) # test sin
      #print(sinTest)

      glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
      glEnable(GL_DEPTH_TEST)

      # Creating the ground
      glColor3f(0.2, 0.5, 0.2)
      glPushMatrix()
      glTranslatef(0, 0, 0)
      glScalef(20, 0.1, 20)

      glBegin(GL_QUADS)
      glVertex3f(-1, 0, -1)
      glVertex3f(1, 0, -1)
      glVertex3f(1, 0, 1)
      glVertex3f(-1, 0, 1)
      glEnd()
      glPopMatrix()

      #glColor3f(1, 0, 0)
      #glPushMatrix()
      #ball.draw()
      #ball.updatePos(move_x, move_y, move_z)
      #glPopMatrix()

      for i in sphereList:
         glPushMatrix()
         i.draw()
         glPopMatrix()

      pygame.display.flip()
      pygame.time.wait(10)

main()
