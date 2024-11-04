import pygame
import time

from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import cube

verticies = (
   (1, -1, -1),
   (1, 1, -1),
   (-1, 1, -1),
   (-1, -1, -1),
   (1, -1, 1),
   (1, 1, 1),
   (-1, -1, 1),
   (-1, 1, 1)
)

edges = (
   (0,1),
   (0,3),
   (0,4),
   (2,1),
   (2,3),
   (2,7),
   (6,3),
   (6,4),
   (6,7),
   (5,1),
   (5,4),
   (5,7)
)

class Ground:
   def __init__(self, width, depth):
      self.width = width
      self.depth = depth

   def paint(self):
      glColor3f(0.2, 0.5, 0.2)
      glPushMatrix()
      glTranslatef(0, 0, 0)
      glScalef(self.width, 0.1, self.depth)

      glBegin(GL_QUADS)
      glVertex3f(-1, 0, -1)
      glVertex3f(1, 0, -1)
      glVertex3f(1, 0, 1)
      glVertex3f(-1, 0, 1)
      glEnd()

      glPopMatrix()

class Cube:
   def __init__(self, name, pos_x, pos_y, pos_z, height, width, depth):
      self.name = name
      self.pos_x = pos_x
      self.pos_y = pos_y
      self.pos_z = pos_z
      self.height = height
      self.width = width
      self.depth = depth

   def paint(self):
      #glColor3f(0.8, 0.2, 0.2)
      glPushMatrix()

      glTranslatef(self.pos_x, self.pos_y, self.pos_z)
      glScalef(self.width, self.height, self.depth)

      glBegin(GL_QUADS)

      # Front face
      glVertex3f(-0.5, -0.5, 0.5)
      glVertex3f(0.5, -0.5, 0.5)
      glVertex3f(0.5, 0.5, 0.5)
      glVertex3f(-0.5, 0.5, 0.5)

      # Back face
      glVertex3f(-0.5, -0.5, -0.5)
      glVertex3f(-0.5, 0.5, -0.5)
      glVertex3f(0.5, 0.5, -0.5)
      glVertex3f(0.5, -0.5, -0.5)

      # Left face
      glVertex3f(-0.5, -0.5, -0.5)
      glVertex3f(-0.5, -0.5, 0.5)
      glVertex3f(-0.5, 0.5, 0.5)
      glVertex3f(-0.5, 0.5, -0.5)

      # Right face
      glVertex3f(0.5, -0.5, -0.5)
      glVertex3f(0.5, 0.5, -0.5)
      glVertex3f(0.5, 0.5, 0.5)
      glVertex3f(0.5, -0.5, 0.5)

      # Top face
      glVertex3f(-0.5, 0.5, -0.5)
      glVertex3f(0.5, 0.5, -0.5)
      glVertex3f(0.5, 0.5, 0.5)
      glVertex3f(-0.5, 0.5, 0.5)

      # Bottom face
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

   def draw(self):
      #glTranslatef(1, 0.0, 0.0)
      glColor3f(0.9, 0.1, 0.1)
      head = Cube("head", self.x_cord, self.y_cord+1, self.z_cord-5, 0.5, 0.5, 0.5)
      head.paint()

      glColor3f(0.1, 0.9, 0.1)
      body = Cube("body", self.x_cord, self.y_cord, self.z_cord-5, 1.5, 1, 0.5)
      body.paint()

      glColor3f(0.1, 0.1, 0.9)
      left_arm = Cube("left_arm", self.x_cord-0.8, self.y_cord, self.z_cord-5, 1, 0.5, 0.5)
      left_arm.paint()

      glColor3f(0.1, 0.1, 0.9)
      right_arm = Cube("right_arm", self.x_cord+0.8, self.y_cord, self.z_cord-5, 1, 0.5, 0.5)
      right_arm.paint()

      glColor3d(0.9, 0.1, 0.9)
      left_leg = Cube("left_leg", self.x_cord-0.3, self.y_cord-1.3, self.z_cord-5, 1, 0.5, 0.5)
      left_leg.paint()

      glColor3d(0.9, 0.1, 0.9)
      right_leg = Cube("right_leg", self.x_cord+0.3, self.y_cord-1.3, self.z_cord-5, 1, 0.5, 0.5)
      right_leg.paint()

def main():
   pygame.init()
   display = (800,600)
   pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

   gluPerspective(90, (display[0]/display[1]), 0.1, 50.0)

   gluLookAt(0.0, 6.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

   ground = Ground(20, 20)
   cube1 = Cube("Cube1", 0, 0, -5, 1, 1, 1)
   #glTranslatef(19, 0, 0
   glTranslatef(0, 2, 0)

   bob_x = 0.0
   bob_y = 0.0
   bob_z = 0.0

   upFlag = 0
   downFlag = 0
   leftFlag = 0
   rightFlag  = 0
   spaceFlag = 0

   while True:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
            quit()

         keys = pygame.key.get_pressed()
         if event.type == pygame.KEYDOWN:
            if keys[pygame.K_LEFT]:
               print("Left pressed")
               leftFlag = 1
            if keys[pygame.K_RIGHT]:
               print("Right pressed")
               rightFlag = 1
            if keys[pygame.K_UP]:
               print("Up pressed")
               upFlag = 1
            if keys[pygame.K_DOWN]:
               print("Down pressed")
               downFlag = 1
            if keys[pygame.K_SPACE]:
               print("Space pressed")
               spaceFlag = 1


         if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
               print("Left released")
               leftFlag = 0
            if event.key == pygame.K_RIGHT:
               print("Right released")
               rightFlag = 0
            if event.key == pygame.K_UP:
               print("Up released")
               upFlag = 0
            if event.key == pygame.K_DOWN:
               print("Down released")
               downFlag = 0
            if event.key == pygame.K_SPACE:
               print("Space released")
               spaceFlag = 0

      if leftFlag == 1:
         bob_x = bob_x - 0.05
      if rightFlag == 1:
         bob_x = bob_x + 0.05
      if upFlag == 1:
         bob_z = bob_z - 0.05
      if downFlag == 1:
         bob_z = bob_z + 0.05
      if spaceFlag == 1:
         bob_y = bob_y + 1
         time.sleep(0.5)
         bob_y = bob_y - 1

      bob = Character("bob", bob_x, bob_y, bob_z)
      glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
      ground.paint()
      bob.draw()
      pygame.display.flip()
      pygame.time.wait(10)

main()
