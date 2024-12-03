# 3D Zombie Game
# By Richard Evans R11677817
#
# This is a 3D Game that has you defend yourself against waves of zombies. Your objective
# is to survive as long as you can and rack up as many points as you can.
#
# Controls:
# =========
# "A" key to move left
# "D" key to move right
# "Space" bar to shoot
# "1" to upgrade weapons fire rate for 20 points
#
# Guide:
# =========
# When starting the game, an initial zombie will be spawned, after a random interval of time, more
# zombies will start spawning. There are 4 stages, the first being the first 15 seconds, the second
# being from 15 to 30 seconds, the third being from 30 to 60 seconds, and the fourth and final being
# 60 seconds and above. At each stage, zombies because more durable, requiring more shots to take down.
# At stage 4, zombies will also gain a boost in speed.
# For 20 points, you can upgrade your weapon pressing "1" on your keyboard. This will increase your rate
# of fire.
# Your objective is to survive.

import random
import pygame
import time
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


zombieList = [] # list to store all created zombies
bulletList = [] # list to store all created bullets


# Sphere class
#
# Used in the creation of bullets
class Sphere:
    def __init__(self, name, radius, x_cord, y_cord, z_cord):
        self.name = name
        self.radius = radius
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.z_cord = z_cord
        self.time = 0
        self.speed = 1
        bulletList.append(self)
        self.hit = 0
        self.damage = 25

    # draw function
    #
    # Takes time as input
    # Used to draw the sphere and set the coordinates and transformations
    def draw(self, time):
        self.time = time
        glColor3f(0.1, 0.1, 0.1)
        glPushMatrix()
        glTranslatef(self.x_cord, self.y_cord, self.z_cord)
        sphere = gluNewQuadric()
        gluSphere(sphere, self.radius, 32, 32)
        glPopMatrix()

    # shoot function
    #
    # Takes no input
    # Used to set constant movement along z cord,
    # Uses self.speed to subtract from z cord, making bullet move away from screen
    def shoot(self):
        self.z_cord = self.z_cord - self.speed


# Cube class
#
# Used in the creation of zombies, characters, and environment
class Cube:
    def __init__(self, name, height, width, depth, texture=None):
        self.name = name
        self.texture = texture
        self.height = height
        self.width = width
        self.depth = depth

    # draw function
    #
    # Takes no input
    # Draws cube and applies texturing by using loadTexture function
    def draw(self):
        if self.texture:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture)
        else:
            glDisable(GL_TEXTURE_2D)
        glPushMatrix()
        glScalef(self.width, self.height, self.depth)

        glBegin(GL_QUADS)

        # Front of cube
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-0.5, 0.5, 0.5)

        # Top of cube
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-0.5, 0.5, -0.5)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(0.5, 0.5, -0.5)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-0.5, 0.5, 0.5)

        # Bottom of cube
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(0.5, -0.5, 0.5)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(0.5, -0.5, -0.5)

        # Back of cube
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-0.5, 0.5, -0.5)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(0.5, 0.5, -0.5)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(0.5, -0.5, -0.5)

        # Left side of cube
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-0.5, 0.5, -0.5)

        # Right side of cube
        glTexCoord2f(0.0, 0.0)
        glVertex3f(0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(0.5, 0.5, -0.5)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(0.5, -0.5, 0.5)

        glEnd()

        glPopMatrix()


# Zombie class
#
# Uses cube class to create zombies
# Zombies will spawn and move towards the player in random intervals
# Depending on the time, zombies are stronger and faster
class Zombie:
    def __init__(self, name, x_cord, y_cord, z_cord, faceTexture):
        self.exploded = 0 # flag to see if zombie is exploded
        self.explodedTime = 0 # store the time in which zombie was exploded
        self.name = name # sets name
        self.x_cord = x_cord # sets current x coordinate
        self.y_cord = y_cord # sets current y coordinate
        self.z_cord = z_cord # sets current z coordinate
        self.time = 0 # stores current game time
        self.isMoving = 0 # flag to check if zombie is moving
        self.speed = 0.03 # sets speed, used in adding or subtracting from a coordinate
        self.collided = False # flag to see if zombie has collided with bullet
        self.health = 200 # Starting health set to 200
        self.face = faceTexture
        zombieList.append(self) # Adding every new zombie to the zombieList for rendering in main


    # Draw function to render zombie
    #
    # Takes time as input
    # Uses Cube class to render body parts
    # Makes various checks to create animations
    def draw(self, time):
        self.time = time
        glPushMatrix()
        glTranslatef(self.x_cord, self.y_cord, self.z_cord)

        # Creating head of zombie
        # Putting it at y=1 to go above body
        glColor3f(1, 1, 1)
        glPushMatrix()
        if self.exploded == 0:
            glTranslatef(0, 1, 0)
            # head = Cube("head", 0.5, 0.5, 0.5)
            # head.draw()
        elif self.exploded == 1:
            # print(time)
            explodeRate = ((self.time - self.explodedTime) * 100)
            # print(explodeRate)

            glTranslatef(0, explodeRate, 0)

        head = Cube("head", 0.5, 0.5, 0.5, self.face)
        head.draw()
        glPopMatrix()

        # Creating body of zombie
        # Putting it at y=0 to act as center
        glColor3f(0.21, 0.46, 0.53)
        glPushMatrix()
        if self.exploded == 0: # if not exploded, standard positioning
            glTranslatef(0, 0, 0)
        elif self.exploded == 1: # if exploded, place body on ground to act "dead"
            glTranslatef(0, -1.5, 0)
            glRotate(90, 1, 0, 0)
        body = Cube("body", 1.5, 1, 0.5)
        body.draw()
        glPopMatrix()

        # Creating left arm of zombie
        # Putting at x=-0.8 and y = 0 to go to left of body
        glColor3f(0.47, 0.49, 0.3)
        glPushMatrix()
        if self.exploded == 0: # if not exploded, standard positioning
            glTranslatef(-0.8, 0.3, 0)
        elif self.exploded == 1: # if exploded, translate and rotate the arm outwards
            # print(time)
            explodeRate = 0.8 + ((time - self.explodedTime) * 80)
            glTranslatef(-explodeRate, explodeRate, 0)
            glRotatef(30 * explodeRate, 1, 1, 1)

        glRotatef(-90, 1, 0, 0)
        left_arm = Cube("left_arm", 1, 0.5, 0.5)
        left_arm.draw()
        glPopMatrix()

        # Creating right arm of zombie
        # Putting at x=0.8 and y = 0 to go to right of body
        glColor3f(0.47, 0.49, 0.3)
        glPushMatrix()
        if self.exploded == 0: # if not exploded, standard positioning
            glTranslatef(0.8, 0.3, 0)
        elif self.exploded == 1: # if exploded, translate and rotate the arm outwards
            # print(time)
            explodeRate = 0.8 + ((time - self.explodedTime) * 80)
            glTranslatef(explodeRate, explodeRate, 0)
            glRotatef(30 * explodeRate, 1, 1, 1)

        glRotatef(-90, 1, 0, 0)
        right_arm = Cube("right_arm", 1, 0.5, 0.5)
        right_arm.draw()
        glPopMatrix()

        # Creating left leg of zombie
        # Putting at x = -0.3 and y = -1.3 to go left and below body
        glColor3d(0.76, 0.69, 0.57)
        glPushMatrix()
        if self.exploded == 0: # if not exploded, standard positioning
            glTranslatef(-0.3, -1.3, 0)
        elif self.exploded == 1: # if exploded, translate and rotate the leg outwards
            # print(time)
            explodeRate = 0.3 + ((time - self.explodedTime) * 80)
            glTranslatef(-explodeRate, -explodeRate, 0)
            glRotatef(30 * explodeRate, 1, 1, 1)

        if self.isMoving == 1:
            glRotatef(-(np.sin(self.time * 10)) * 20, 1, 0, 0)
        left_leg = Cube("left_leg", 1, 0.5, 0.5)
        left_leg.draw()
        glPopMatrix()

        # Creating right leg of zombie
        # Putting at x = 0.3 and y = -1.3 to go right and below body
        glColor3d(0.76, 0.69, 0.57)
        glPushMatrix()
        if self.exploded == 0: # if not exploded, standard positioning
            glTranslatef(0.3, -1.3, 0)
        elif self.exploded == 1: # if exploded, translate and rotate the leg outwards
            # print(time)
            explodeRate = 0.3 + ((time - self.explodedTime) * 80)
            glTranslatef(explodeRate, -explodeRate, 0)
            glRotatef(30 * explodeRate, 1, 1, 1)

        if self.isMoving == 1: # if moveing flag is set, set slight rotation for leg movement animation
            glRotatef(np.sin(self.time * 10) * 20, 1, 0, 0) # using sin for leg to move back and forward
        right_leg = Cube("right_leg", 1, 0.5, 0.5)
        right_leg.draw()
        glPopMatrix()

        glPopMatrix()


    # zombieMove function
    #
    # Takes no input
    # When called, sets is moving flag to 1 to initiate moving animations
    # Sets constant movement along z axis to move closer to camera
    def zombieMove(self):
        self.isMoving = 1
        self.z_cord = self.z_cord + self.speed


    # explode function
    #
    # Takes no input
    # If called, sets exploded flag to 1 and sets the
    # explodedtime to the current time when called
    def explode(self):
        self.exploded = 1
        self.explodedTime = self.time


    # Difficulty function
    #
    # Takes no input
    # Checks time and changes zombie health
    def difficulty(self):
        if self.time > 60: # If time is greater than 60 seconds set health to 250
            self.health = 250
        elif self.time > 30: # If time greater than 30 seconds, set to 200
            self.health = 200
        else:
            self.health = 100 # Otherwise, set to base 100


# Shooter class
#
# Class used to create the character the player will control
# Uses the cube class for body part creation
class Shooter:
    def __init__(self, name, x_cord, y_cord, z_cord):
        self.leftFlag = 0
        self.rightFlag = 0
        self.upFlag = 0
        self.downFlag = 0
        self.name = name
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.z_cord = z_cord
        self.time = 0
        self.isMoving = 0
        self.speed = 0.1
        self.lastShot = 0
        self.fireRate = 0.5
        self.bulletCount = 0


    # Draw function to render character
    #
    # Uses Cube class to render body parts
    def draw(self, time):
        self.time = time
        glPushMatrix()
        glTranslatef(self.x_cord, self.y_cord, self.z_cord)

        # Creating head of character
        # Putting it at y=1 to go above body
        glColor3f(0.82, 0.71, 0.55)
        glPushMatrix()
        glTranslatef(0, 1, 0)
        head = Cube("head", 0.5, 0.5, 0.5)
        head.draw()

        glPopMatrix()

        # Creating body of character
        # Putting it at y=0 to act as center
        glColor3f(0.50, 0, 0)
        glPushMatrix()
        glTranslatef(0, 0, 0)
        body = Cube("body", 1.5, 1, 0.5)
        body.draw()
        glPopMatrix()

        # Creating left arm of character
        # Putting at x=-0.8 and y = 0 to go to left of body
        glColor3f(0.50, 0, 0)
        glPushMatrix()
        glTranslatef(-0.8, 0, 0)
        if self.isMoving == 0: # if moving, set arm to swing
            glRotatef(np.sin(self.time) * 5, 0, 0, 1)
        else:
            glRotatef(np.sin(self.time * 10) * 20, 1, 0, 0)
        left_arm = Cube("left_arm", 1, 0.5, 0.5)
        left_arm.draw()
        glPopMatrix()

        # Creating right arm of character
        # Putting at x=0.8 and y = 0 to go to right of body
        glColor3f(0.50, 0, 0)
        glPushMatrix()
        glTranslatef(0.6, 0.5, -0.4)
        glRotatef(90, 1, 0, 0)
        right_arm = Cube("right_arm", 1, 0.5, 0.5)
        right_arm.draw()
        glPopMatrix()

        # Creating left leg of character
        # Putting at x = -0.3 and y = -1.3 to go left and below body
        glColor3d(0.43, 0.56, 0.69)
        glPushMatrix()
        glTranslatef(-0.3, -1.3, 0)
        if self.isMoving == 1: # if moving, set leg to move back and forward
            glRotatef(-(np.sin(self.time * 10)) * 20, 1, 0, 0)
        left_leg = Cube("left_leg", 1, 0.5, 0.5)
        left_leg.draw()
        glPopMatrix()

        # Creating right leg of character
        # Putting at x = 0.3 and y = -1.3 to go right and below body
        glColor3d(0.43, 0.56, 0.69)
        glPushMatrix()
        glTranslatef(0.3, -1.3, 0)
        if self.isMoving == 1: # if moving, set leg to move back and forward
            glRotatef(np.sin(self.time * 10) * 20, 1, 0, 0)
        right_leg = Cube("right_leg", 1, 0.5, 0.5)
        right_leg.draw()
        glPopMatrix()

        glPopMatrix()


    # move used to set user control movement
    #
    # Takes leftFlag, rightFlag, and spaceFlag input
    def move(self, leftFlag, rightFlag, spaceFlag):
        self.isMoving = leftFlag or rightFlag

        if leftFlag == 1:  # if left key bind is active, then subtract from characters x coordinate to move left
            if -10 < self.x_cord:
                self.x_cord = self.x_cord - self.speed
            else:
                print(f"Hitting barrier x:{self.x_cord}")
        if rightFlag == 1:  # Opposite if moving right
            if 10 > self.x_cord:
                self.x_cord = self.x_cord + self.speed
            else:
                print(f"Hitting barrier x:{self.x_cord}")
        if spaceFlag == 1:
            current_time = time.time()
            if current_time - self.lastShot >= self.fireRate:
                # print("Shooting")
                bullet = Sphere(f"bullet{self.bulletCount}", 0.2, self.x_cord + 0.6, 2, 7)
                self.bulletCount = self.bulletCount + 1
                bulletList.append(bullet)
                self.lastShot = current_time


# drawText function
#
# Takes position and text to render as input
# Function to render text over opengl rendering. Takes posiitoning x, y, and z coordinates as well as text
# to render
def drawText(position, textString):
    font = pygame.font.Font(None, 64)
    textSurface = font.render(textString, True, (255, 255, 255, 255), (0, 0, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


# loadTexture function
#
# Takes a texture input
# Loads and binds a texture image to a surface
def loadTexture(texture):
    textureSurface = pygame.image.load(texture)
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    glEnable(GL_TEXTURE_2D)
    textureID = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, textureID)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    return textureID


# Main
#
# Create opengl renderings
def main():
    pygame.init()
    display = (1000, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(90, (display[0] / display[1]), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    # Game flags
    leftFlag = 0 # Indicates button to move left is being pressed
    rightFlag = 0 # Indicates button to move right is being pressed
    spaceFlag = 0 # Indiciates button to jump is being pressed
    activeObjectIndex = 0 # Index for active object
    explodeFlag = 0 # Flag to initiate explosion of object
    zombieNum = 0 # Flag to keep number of zombies spawned
    next_spawn_time = 5 # Amount of time in seconds for next zombie spawn to occur
    despawnTime = 10 # Amount of time in seconds for next zombie despawn to occur
    pastZombieList = [] # List to hold zombies that are dead (exploded)
    gameFlag = True # Flag to keep game running
    totalPoints = 0 # Points gained by player
    stage = 1 # Stage number. Stage 1: First 15 seconds. Stage 2: 15-30 seconds. Stage 3: 30-60 seconds. Stage 4: >60 seconds.

    # Texture creation
    zombieFace = loadTexture("big-zombie-face.png")
    ground = loadTexture('road-texture.png')
    sky = loadTexture('sky_texture.jpg')
    barrierTexture = loadTexture('concrete_texture.jpg')

    # Object initialization
    zombie = Zombie("zombie", 0, 1.8, -20, zombieFace) # Initial zombie that spawns
    bob = Shooter("bob", 0, 1.8, 7) # Bob, A.K.A the player
    barrier_left = Cube("b_left", 3, 0.5, 90, barrierTexture) # Left barrier of map
    barrier_right = Cube("b_right", 3, 0.5, 90, barrierTexture) # Right barrier of map
    ground = Cube("ground", 0.1, 21, 90, ground) # Ground of map
    skybox = Cube("sky", 100, 150, 100, sky) # Sky around map

    activeObject = zombieList[activeObjectIndex]
    # print(objectList[0].name)
    # print(activeObject.x_cord)

    # Main game loop
    while gameFlag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Using pygame keys to find keys being pressed
            # If specified key is pressed, its flag is set
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    # print("Left pressed")
                    leftFlag = 1
                if event.key == pygame.K_d:
                    # print("Right pressed")
                    rightFlag = 1
                if event.key == pygame.K_w:
                    # print("Up pressed")
                    upFlag = 1
                if event.key == pygame.K_s:
                    # print("Down pressed")
                    downFlag = 1
                if event.key == pygame.K_SPACE:
                    # print("Space pressed")
                    spaceFlag = 1
                if event.key == pygame.K_1:
                    if totalPoints >= 20:
                        totalPoints = totalPoints - 20
                        if bob.fireRate > 0.1:
                            bob.fireRate = bob.fireRate / 2
                    else:
                        print("Not enough points")
                if event.key == pygame.K_LEFT:
                    print("Left cam pressed")

            # Using pygame keys to find keys released after being pressed
            # If specified key is released its flag is reset
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    # print("Left released")
                    leftFlag = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    # print("Right released")
                    rightFlag = 0
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    # print("Up released")
                    upFlag = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    # print("Down released")
                    downFlag = 0
                if event.key == pygame.K_SPACE:
                    # print("Space released")
                    spaceFlag = 0

        glLoadIdentity()
        gluLookAt(0, 10, 10,
                  0, 0, 0,
                  0, 1, 0)

        time = pygame.time.get_ticks() / 1000  # returns time in milliseconds / 1000 to get seconds
        # print(f"Current Time: {time}")
        # print(f"Next Spawn Time: {next_spawn_time}")
        if time >= next_spawn_time and len(zombieList) < 30:
            newZombie = Zombie(f"zombie{zombieNum}", random.randint(-5, 5), 2, -20, zombieFace)
            zombieNum = zombieNum + 1

            if time > 60:
                next_spawn_time = time + 0.05
                # print("Spawn time: 60")
            elif time > 30:
                next_spawn_time = time + 0.5
                # print("Spawn time: 30")
            elif time > 15:
                next_spawn_time = time + 1
                # print("Spawn time: 15")
            else:
                next_spawn_time = time + 1.5
                # print("Spawn time: Base")

        # looping through zombieList to apply the self moving functionality
        # and check for bullet collision
        for index, zombie in enumerate(zombieList):
            glPushMatrix()
            if zombie.exploded == 0:
                zombie.zombieMove()
            else:
                pastZombieList.append(zombie)  # add to pastZombieList
                zombieList.remove(zombie)  # remove from zombieList
                totalPoints = totalPoints + 1

                activeObjectIndex = len(zombieList) - 1
            glPopMatrix()

            if explodeFlag == 1: # explode zombie is explodeFlag is set
                zombie.explode()

            if time > 60: # increase zombie speed after 60 seconds
                zombie.speed = 0.07
                #print(f"Zombie speed: {zombie.speed}")

            # looping through bullet list to check for hits
            for bullet in bulletList:
                if zombie.x_cord - 2 < bullet.x_cord < zombie.x_cord + 2 and zombie.z_cord - 1 < bullet.z_cord < zombie.z_cord + 1:
                    # if the game time is greater than 60, set the stage to 4 and reduce bullet damage
                    if time > 60:
                        stage = 4
                        #print(f"Bullet dmg: {bullet.damage}")
                        #print(f"Zombie health: {zombie.health}")
                    # if the game time is greater than 30, set the stage to 3 and reduce bullet damage
                    elif time > 30:
                        stage = 3
                        bullet.damage = 25
                        #print(f"Bullet dmg: {bullet.damage}")
                        #print(f"Zombie health: {zombie.health}")
                    # if the game time is greater than 15, set the stage to 2 and reduce bullet damage
                    elif time > 15:
                        stage = 2
                        bullet.damage = 50
                        #print(f"Bullet dmg: {bullet.damage}")
                        #print(f"Zombie health: {zombie.health}")
                    # Otherwise, the initial stage is 1, and bullets do full damage (100)
                    else:
                        stage = 1
                        bullet.damage = 100
                        #print(f"Bullet dmg: {bullet.damage}")
                        #print(f"Zombie health: {zombie.health}")

                    # If zombies health is equal to or below 0, explode them
                    if zombie.health <= 0:
                        zombie.explode()

                    zombie.health = zombie.health - bullet.damage # zombie health set
                    # print(f"{i.name} health: {i.health}")
                    # print(bullet.name)
                    bullet.hit = True # if coordinates of bullet and a zombie match, bullet is hit

        # check coordinates of every object
        # for i in zombieList:
        #     print(f"Object\nX: {i.x_cord}\nY: {i.y_cord}\nZ: {i.z_cord}\n\n")

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)

        # Creating the sky
        glColor3f(1, 1, 1)
        glPushMatrix()
        glRotatef(-45, 1, 0, 0)
        glTranslatef(0, 0, -80)
        skybox.draw()
        glPopMatrix()

        # Creating the ground
        glColor3f(1, 1, 1)
        glPushMatrix()
        ground.draw()
        glPopMatrix()

        # Drawing left barrier and positioning to left
        glColor3f(0.2, 0.2, 0.2)
        glPushMatrix()
        glTranslatef(-11, 1, 0)
        barrier_left.draw()
        glPopMatrix()

        # Drawing right barrier and positioning to right
        glColor3f(0.2, 0.2, 0.2)
        glPushMatrix()
        glTranslatef(11, 1, 0)
        barrier_right.draw()
        glPopMatrix()

        # Looping through zombies in the zombieList and applying draw function to render each
        for zombie in zombieList:
            glPushMatrix()
            zombie.draw(time)
            glPopMatrix()

            # If the zombies make it to the player (z cord of 7) the game ends
            if zombie.z_cord >= 7:
                gameFlag = False
                print("Game Over")

            # cleanup when out of view
            if zombie.z_cord >= 10:
                zombieList.remove(zombie)

        # Looping through pastZombieList to continue rendering exploded objects
        for zombie in pastZombieList:
            glPushMatrix()
            zombie.draw(time)
            glPopMatrix()

        # Rendering bob (the player)
        glPushMatrix()
        bob.move(leftFlag, rightFlag, spaceFlag)
        bob.draw(time)
        glPopMatrix()

        # Looping through the bulletList to apply draw and shoot function to each bullet
        for bullet in bulletList:
            glPushMatrix()
            bullet.shoot()
            bullet.draw(time)
            glPopMatrix()

        # Bullet cleanup
        for bullet in bulletList:
            if bullet.z_cord < -30: # if the bullet gets to z cord of -30 despawn to improve performance
                bulletList.remove(bullet)
            elif bullet.hit: # if the bullet hits a zombie despawn
                bulletList.remove(bullet)

        # zombie cleanup
        for zombie in pastZombieList:
            if time > despawnTime:  # if the current time is greater than the set despawn time, remove dead zombies
                pastZombieList.remove(zombie)

                if time > 30:   # if the game time is over 30 seconds, make the despawn time the same as the next spawn time
                    despawnTime = next_spawn_time
                else:   # otherwise set the despawn time to 2 seconds ahead
                    despawnTime = time + 2

        #print(f"Fire Rate: {bob.fireRate}")

        # Using drawText function to render total points, the time, and the current stage to the screen
        drawText([-2, 9, 0], f"Points: {totalPoints}") # positioned to middle of screen
        drawText([-12, 9, 0], f"Time: {time}") # positioned to left of screen
        drawText([8, 9, 0], f"Stage: {stage}") # positioned to right of screen

        pygame.display.flip()
        pygame.time.wait(10)


main()
