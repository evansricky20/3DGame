import random

import pygame
import time
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

objectList = []

class Sphere:
   def __init__(self, name, radius, x_cord, y_cord, z_cord):
      self.name = name
      self.radius = radius
      self.x_cord = x_cord
      self.y_cord = y_cord
      self.z_cord = z_cord
      self.time = 0
      objectList.append(self)
      self.red = random.uniform(0, 1)
      self.green = random.uniform(0, 1)
      self.blue = random.uniform(0, 1)

   def draw(self, time):
      self.time = time
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

   def orbit(self, radius, speed):
      self.x_cord = radius * np.cos(speed * self.time)
      self.z_cord = radius * np.sin(speed * self.time)


class Cube:
   def __init__(self, name, height, width, depth):
      self.name = name

      self.height = height
      self.width = width
      self.depth = depth

   def draw(self):

      glPushMatrix()
      glScalef(self.width, self.height, self.depth)

      glBegin(GL_QUADS)

      glVertex3f(-0.5, -0.5, 0.5)
      glVertex3f(0.5, -0.5, 0.5)
      glVertex3f(0.5, 0.5, 0.5)
      glVertex3f(-0.5, 0.5, 0.5)

      glVertex3f(-0.5, -0.5, -0.5)
      glVertex3f(-0.5, 0.5, -0.5)
      glVertex3f(0.5, 0.5, -0.5)
      glVertex3f(0.5, -0.5, -0.5)

      glVertex3f(-0.5, -0.5, -0.5)
      glVertex3f(-0.5, -0.5, 0.5)
      glVertex3f(-0.5, 0.5, 0.5)
      glVertex3f(-0.5, 0.5, -0.5)

      glVertex3f(0.5, -0.5, -0.5)
      glVertex3f(0.5, 0.5, -0.5)
      glVertex3f(0.5, 0.5, 0.5)
      glVertex3f(0.5, -0.5, 0.5)

      glVertex3f(-0.5, 0.5, -0.5)
      glVertex3f(0.5, 0.5, -0.5)
      glVertex3f(0.5, 0.5, 0.5)
      glVertex3f(-0.5, 0.5, 0.5)

      glVertex3f(-0.5, -0.5, -0.5)
      glVertex3f(-0.5, -0.5, 0.5)
      glVertex3f(0.5, -0.5, 0.5)
      glVertex3f(0.5, -0.5, -0.5)

      glEnd()

      glPopMatrix()


class Character:
   def __init__(self, name, x_cord, y_cord, z_cord):
      self.name = name
      self.x_cord = x_cord
      self.y_cord = y_cord
      self.z_cord = z_cord
      self.time = 0
      self.isMoving = 0
      objectList.append(self)

   # Draw function to render character
   #
   # Uses Cube class to render body parts
   def draw(self, time):
      self.time = time
      glPushMatrix()
      glTranslatef(self.x_cord, self.y_cord, self.z_cord)
      # Creating head of character
      # Putting it at y=1 to go above body
      glColor3f(0.9, 0.1, 0.1)
      glPushMatrix()
      glTranslatef(0, 1, 0)
      head = Cube("head", 0.5, 0.5, 0.5)
      head.draw()
      glPopMatrix()

      # Creating body of character
      # Putting it at y=0 to act as center
      glColor3f(0.1, 0.9, 0.1)
      glPushMatrix()
      glTranslatef(0, 0, 0)
      body = Cube("body", 1.5, 1, 0.5)
      body.draw()
      glPopMatrix()

      # Creating left arm of character
      # Putting at x=-0.8 and y = 0 to go to left of body
      glColor3f(0.1, 0.1, 0.9)
      glPushMatrix()
      glTranslatef(-0.8, 0, 0)
      if self.isMoving == 0:
         glRotatef(np.sin(self.time) * 5, 0, 0, 1)
      else:
         glRotatef(np.sin(self.time * 10) * 20, 1, 0, 0)
      left_arm = Cube("left_arm", 1, 0.5, 0.5)
      left_arm.draw()
      glPopMatrix()

      # Creating right arm of character
      # Putting at x=0.8 and y = 0 to go to right of body
      glColor3f(0.1, 0.1, 0.9)
      glPushMatrix()
      glTranslatef(0.8, 0, 0)
      if self.isMoving == 0:
         glRotatef(-(np.sin(self.time)) * 5, 0, 0, 1)
      else:
         #print("Bob is moving")
         glRotatef(-(np.sin(self.time * 10)) * 20, 1, 0, 0)
      right_arm = Cube("right_arm", 1, 0.5, 0.5)
      right_arm.draw()
      glPopMatrix()

      # Creating left leg of character
      # Putting at x = -0.3 and y = -1.3 to go left and below body
      glColor3d(0.9, 0.1, 0.9)
      glPushMatrix()
      glTranslatef(-0.3, -1.3, 0)
      if self.isMoving == 1:
         glRotatef(-(np.sin(self.time * 10)) * 20, 1, 0, 0)
      left_leg = Cube("left_leg", 1, 0.5, 0.5)
      left_leg.draw()
      glPopMatrix()

      # Creating right leg of character
      # Putting at x = 0.3 and y = -1.3 to go right and below body
      glColor3d(0.9, 0.1, 0.9)
      glPushMatrix()
      glTranslatef(0.3, -1.3, 0)
      if self.isMoving == 1:
         glRotatef(np.sin(self.time * 10) * 20, 1, 0, 0)
      right_leg = Cube("right_leg", 1, 0.5, 0.5)
      right_leg.draw()
      glPopMatrix()

      glPopMatrix()


   def move(self, leftFlag, rightFlag, upFlag, downFlag, spaceFlag, ctrlFlag):
      self.isMoving = leftFlag or rightFlag or upFlag or downFlag
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

   glMatrixMode(GL_PROJECTION)
   gluPerspective(90, (display[0]/display[1]), 0.1, 50.0)
   glMatrixMode(GL_MODELVIEW)
   #gluLookAt(0.0, 5.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

   # Flags to get status of bob
   upFlag = 0
   downFlag = 0
   leftFlag = 0
   rightFlag  = 0
   spaceFlag = 0
   ctrlFlag = 0
   activeObjectIndex = 0
   #activeObject = objectList[activeObjectIndex]

   ball = Sphere("ball1", 1, 3, 1, 0)
   ball2 = Sphere("ball2", 2, -3, 1, 0)
   #ball3 = Sphere("ball3", 1, 4, 2, 0)
   bob = Character("bob", 0, 2, -5)

   activeObject = objectList[activeObjectIndex]
   #print(objectList[0].name)
   print(activeObject.x_cord)

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
               if activeObjectIndex == 0:
                  print("Current index 0, cannot go out of range.")
               else:
                  activeObjectIndex = activeObjectIndex - 1
                  activeObject = objectList[activeObjectIndex]
               print(activeObject.name)
            if event.key == pygame.K_PERIOD:
               print("Next pressed")
               if activeObjectIndex == len(objectList)-1:
                  print(f"Current index is {activeObjectIndex}, cannot go out of range.")
               else:
                  activeObjectIndex = activeObjectIndex + 1
                  activeObject = objectList[activeObjectIndex]
               print(activeObject.name)


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

      # camera_offset = [0, 2, -5]
      # camera_pos = [activeObject.x_cord + camera_offset[0],
      #               activeObject.y_cord + camera_offset[1],
      #               activeObject.z_cord + camera_offset[2]]

      pygame.mouse.get_pos()
      # print(pygame.mouse.get_pos())
      mouse_movement = pygame.mouse.get_rel()
      mouse_x_movement = mouse_movement[0]
      mouse_y_movement = mouse_movement[1]


      glLoadIdentity()
      gluLookAt(activeObject.x_cord, activeObject.y_cord+10, activeObject.z_cord+5,
                activeObject.x_cord, activeObject.y_cord, activeObject.z_cord,
                0, 1, 0)

      time = pygame.time.get_ticks() / 1000  # returns time in miliseconds / 1000 to get seconds

      for i in objectList:
         if i.name == activeObject.name:
            glPushMatrix()
            i.move(leftFlag, rightFlag, upFlag, downFlag, spaceFlag, ctrlFlag)
            glPopMatrix()

      for i in objectList:
         if i.name == "ball3":
            i.orbit(3, 1, time)

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


      for i in objectList:
         glPushMatrix()
         i.draw(time)
         glPopMatrix()


      pygame.display.flip()
      pygame.time.wait(10)

main()
