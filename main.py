import random

import pygame
import time
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

zombieList = []
bulletList = []

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

    def draw(self, time):
        self.time = time
        glColor3f(0.1, 0.1, 0.1)
        glPushMatrix()
        glTranslatef(self.x_cord, self.y_cord, self.z_cord)
        sphere = gluNewQuadric()
        gluSphere(sphere, self.radius, 32, 32)
        glPopMatrix()

    def shoot(self):
        self.z_cord = self.z_cord - self.speed


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
        self.exploded = 0
        self.explodedTime = 0
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
        self.direction = 0
        self.speed = 0.03
        self.collided = False
        zombieList.append(self)

    # Draw function to render character
    #
    # Uses Cube class to render body parts
    def draw(self, time):
        self.time = time
        glPushMatrix()
        glTranslatef(self.x_cord, self.y_cord, self.z_cord)
        glRotatef(self.direction, 0, 1, 0)

        # Creating head of character
        # Putting it at y=1 to go above body
        glColor3f(0.27, 0.29, 0.1)
        glPushMatrix()
        if self.exploded == 0:
            glTranslatef(0, 1, 0)
            head = Cube("head", 0.5, 0.5, 0.5)
            head.draw()
        elif self.exploded == 1:
            #print(time)
            explodeRate = ((self.time - self.explodedTime) * 100)
            #print(explodeRate)
            numParts = random.randint(20, 50)
            for i in range(numParts):
                glPushMatrix()
                glTranslatef(random.uniform(-0.5, 0.5) * explodeRate, random.uniform(1, 2) * explodeRate, random.uniform(-0.2, 0.2) * explodeRate)
                glRotatef(30 * explodeRate, 1, 1, 1)
                headParts = Cube(f"head_piece{i}", random.uniform(0.01, 0.1), random.randint(1, 10) / 100, random.randint(1, 10) / 100)
                headParts.draw()
                glPopMatrix()

        glPopMatrix()

        # Creating body of character
        # Putting it at y=0 to act as center
        glColor3f(0.1, 0.9, 0.1)
        glPushMatrix()
        if self.exploded == 0:
            glTranslatef(0, 0, 0)
        elif self.exploded == 1:
            glTranslatef(0, -1, 0)
            glRotate(90, 1, 0, 0)
        body = Cube("body", 1.5, 1, 0.5)
        body.draw()
        glPopMatrix()

        # Creating left arm of character
        # Putting at x=-0.8 and y = 0 to go to left of body
        glColor3f(0.27, 0.29, 0.1)
        glPushMatrix()
        if self.exploded == 0:
            glTranslatef(-0.8, 0.3, 0)
        elif self.exploded == 1:
            #print(time)
            explodeRate = 0.8 + ((time - self.explodedTime) * 80)
            glTranslatef(-explodeRate, explodeRate, 0)
            glRotatef(30 * explodeRate, 1, 1, 1)

        glRotatef(-90, 1, 0, 0)
        left_arm = Cube("left_arm", 1, 0.5, 0.5)
        left_arm.draw()
        glPopMatrix()

        # Creating right arm of character
        # Putting at x=0.8 and y = 0 to go to right of body
        glColor3f(0.27, 0.29, 0.1)
        glPushMatrix()
        if self.exploded == 0:
            glTranslatef(0.8, 0.3, 0)
        elif self.exploded == 1:
            # print(time)
            explodeRate = 0.8 + ((time - self.explodedTime) * 80)
            glTranslatef(explodeRate, explodeRate, 0)
            glRotatef(30 * explodeRate, 1, 1, 1)

        glRotatef(-90, 1, 0, 0)
        right_arm = Cube("right_arm", 1, 0.5, 0.5)
        right_arm.draw()
        glPopMatrix()

        # Creating left leg of character
        # Putting at x = -0.3 and y = -1.3 to go left and below body
        glColor3d(0.9, 0.1, 0.9)
        glPushMatrix()
        if self.exploded == 0:
            glTranslatef(-0.3, -1.3, 0)
        elif self.exploded == 1:
            #print(time)
            explodeRate = 0.3 + ((time - self.explodedTime) * 80)
            glTranslatef(-explodeRate, -explodeRate, 0)
            glRotatef(30 * explodeRate, 1, 1, 1)

        if self.isMoving == 1:
            glRotatef(-(np.sin(self.time * 10)) * 20, 1, 0, 0)
        left_leg = Cube("left_leg", 1, 0.5, 0.5)
        left_leg.draw()
        glPopMatrix()

        # Creating right leg of character
        # Putting at x = 0.3 and y = -1.3 to go right and below body
        glColor3d(0.9, 0.1, 0.9)
        glPushMatrix()
        if self.exploded == 0:
            glTranslatef(0.3, -1.3, 0)
        elif self.exploded == 1:
            # print(time)
            explodeRate = 0.3 + ((time - self.explodedTime) * 80)
            glTranslatef(explodeRate, -explodeRate, 0)
            glRotatef(30 * explodeRate, 1, 1, 1)

        if self.isMoving == 1:
            glRotatef(np.sin(self.time * 10) * 20, 1, 0, 0)
        right_leg = Cube("right_leg", 1, 0.5, 0.5)
        right_leg.draw()
        glPopMatrix()

        glPopMatrix()

    def zombieMove(self):
        self.isMoving = 1
        self.z_cord = self.z_cord + 0.03


    def move(self, leftFlag, rightFlag, upFlag, downFlag, spaceFlag, ctrlFlag):
        self.isMoving = leftFlag or rightFlag or upFlag or downFlag

        if leftFlag == 1:  # if left key bind is active, then subtract from characters x coordiante to move left
            if -10 < self.x_cord:
                self.x_cord = self.x_cord - self.speed
            else:
                print(f"Hitting barrier x:{self.x_cord}")
        if rightFlag == 1:  # Opposite if moving right
            if 10 > self.x_cord:
                self.x_cord = self.x_cord + self.speed
            else:
                print(f"Hitting barrier x:{self.x_cord}")
        if upFlag == 1:
            self.z_cord = self.z_cord - self.speed
        if downFlag == 1:
            if 5 > self.z_cord:
                self.z_cord = self.z_cord + self.speed
            else:
                print(f"Hitting barrier z:{self.z_cord}")
        if spaceFlag == 1:
            self.y_cord = self.y_cord + self.speed
        if ctrlFlag == 1:
            if self.y_cord > 1.8:
                self.y_cord = self.y_cord - self.speed
            else:
                print(f"Hitting barrier y:{self.y_cord}")


    def explode(self):
        self.exploded = 1
        self.explodedTime = self.time



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
        if self.isMoving == 0:
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
        if self.isMoving == 1:
            glRotatef(-(np.sin(self.time * 10)) * 20, 1, 0, 0)
        left_leg = Cube("left_leg", 1, 0.5, 0.5)
        left_leg.draw()
        glPopMatrix()

        # Creating right leg of character
        # Putting at x = 0.3 and y = -1.3 to go right and below body
        glColor3d(0.43, 0.56, 0.69)
        glPushMatrix()
        glTranslatef(0.3, -1.3, 0)
        if self.isMoving == 1:
            glRotatef(np.sin(self.time * 10) * 20, 1, 0, 0)
        right_leg = Cube("right_leg", 1, 0.5, 0.5)
        right_leg.draw()
        glPopMatrix()

        glPopMatrix()


    def move(self, leftFlag, rightFlag, spaceFlag):
        self.isMoving = leftFlag or rightFlag

        if leftFlag == 1:  # if left key bind is active, then subtract from characters x coordiante to move left
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
            current_time = time.time()  # Get current time in seconds
            if current_time - self.lastShot >= self.fireRate:
                #print("Shooting")
                bullet = Sphere("bullet", 0.2, self.x_cord + 0.6, 2, 7)
                bulletList.append(bullet)
                self.lastShot = current_time


def drawText(position, textString):
    font = pygame.font.Font (None, 64)
    textSurface = font.render(textString, True, (255,255,255,255), (0,0,0,255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


def zombieSpawn(zombieNum):
    newZombie = Character(f"zombie{zombieNum}", random.randint(-5, 5), 2, -20)


# Main
#
# Create opengl renderings
def main():
    pygame.init()
    display = (1000, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(90, (display[0] / display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    # gluLookAt(0.0, 5.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    # Flags to get status of bob
    upFlag = 0
    downFlag = 0
    leftFlag = 0
    rightFlag = 0
    spaceFlag = 0
    ctrlFlag = 0
    shiftFlag = 0
    activeObjectIndex = 0
    # activeObject = objectList[activeObjectIndex]
    explodeFlag = 0
    zombieNum = 0
    next_spawn_time = 5
    pastZombieList = []
    gameFlag = True
    totalPoints = 0

    zombie = Character("zombie", 0, 1.8, -20)
    bob = Shooter("bob", 0, 1.8, 7)
    barrier_left = Cube("b_left", 3, 0.5, 90)
    barrier_right = Cube("b_right", 3, 0.5, 90)


    activeObject = zombieList[activeObjectIndex]
    # print(objectList[0].name)
    print(activeObject.x_cord)

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
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    # print("Right pressed")
                    rightFlag = 1
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    # print("Up pressed")
                    upFlag = 1
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    # print("Down pressed")
                    downFlag = 1
                if event.key == pygame.K_SPACE:
                    # print("Space pressed")
                    spaceFlag = 1
                # if event.key == pygame.K_LCTRL:
                #     # print("CTRL pressed")
                #     ctrlFlag = 1
                # if event.key == pygame.K_LSHIFT:
                #     # print("SHIFT pressed")
                #     shiftFlag = 1
                # if event.key == pygame.K_COMMA:
                #     print("Prev pressed")
                #     if activeObjectIndex == 0:
                #         print("Current index 0, cannot go out of range.")
                #     else:
                #         activeObjectIndex = activeObjectIndex - 1
                #         activeObject = zombieList[activeObjectIndex]
                #         print(f'Index: {activeObjectIndex}')
                #     print(activeObject.name)
                # if event.key == pygame.K_PERIOD:
                #     print("Next pressed")
                #     if activeObjectIndex == len(zombieList) - 1:
                #         print(f"Current index is {activeObjectIndex}, cannot go out of range.")
                #     else:
                #         activeObjectIndex = activeObjectIndex + 1
                #         activeObject = zombieList[activeObjectIndex]
                #         print(f'Index: {activeObjectIndex}')
                #     print(activeObject.name)
                if event.key == pygame.K_LEFT:
                    print("Left cam pressed")
                # if event.key == pygame.K_e:
                #     explodeFlag = 1
                # if event.key == pygame.K_1:
                #     newChar = Character(f"bob{bobNum}", random.randint(-5, 5), 2, random.randint(-5,5))
                #     bobNum = bobNum + 1

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
                if event.key == pygame.K_LCTRL:
                    # print("CTRL released")
                    ctrlFlag = 0
                if event.key == pygame.K_LSHIFT:
                    # print("SHIFT released")
                    shiftFlag = 0
                if event.key == pygame.K_e:
                    explodeFlag = 0



        glLoadIdentity()
        # gluLookAt(activeObject.x_cord, activeObject.y_cord + 5, activeObject.z_cord + 5,
        #           activeObject.x_cord, activeObject.y_cord, activeObject.z_cord,
        #           0, 1, 0)
        # gluLookAt(0, 10, 10,
        #           activeObject.x_cord, activeObject.y_cord, activeObject.z_cord,
        #           0, 1, 0)
        gluLookAt(0, 10, 10,
                  0, 0, 0,
                  0, 1, 0)

        time = pygame.time.get_ticks() / 1000  # returns time in miliseconds / 1000 to get seconds
        #print(f"Current Time: {time}")
        #print(f"Next Spawn Time: {next_spawn_time}")
        if time >= next_spawn_time:
            zombieSpawn(zombieNum)  # Spawn a new zombie
            zombieNum = zombieNum + 1
            next_spawn_time = time + random.randint(1, 2)

        for index, i in enumerate(zombieList):
            #if i.name == activeObject.name:
            glPushMatrix()
            if i.exploded == 0:
                #i.move(leftFlag, rightFlag, upFlag, downFlag, spaceFlag, ctrlFlag)
                i.zombieMove()
            else:
                pastZombieList.append(i)  # Add to pastZombieList
                zombieList.remove(i)  # Remove from zombieList
                totalPoints = totalPoints + 1

                activeObjectIndex = len(zombieList) - 1
            glPopMatrix()

            if explodeFlag == 1:
                i.explode()

            for bullet in bulletList:
                if i.x_cord - 2 < bullet.x_cord < i.x_cord + 2 and i.z_cord - 1 < bullet.z_cord < i.z_cord + 1:
                    i.explode()
                    bullet.hit = True

        # check coordinates of every object
        # for i in zombieList:
        #     print(f"Object\nX: {i.x_cord}\nY: {i.y_cord}\nZ: {i.z_cord}\n\n")

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        # Creating the ground
        glColor3f(0.2, 0.5, 0.2)
        glPushMatrix()
        glTranslatef(0, 0, 0)
        glScalef(200, 0.1, 100)

        glBegin(GL_QUADS)
        glVertex3f(-1, 0, -1)
        glVertex3f(1, 0, -1)
        glVertex3f(1, 0, 1)
        glVertex3f(-1, 0, 1)
        glEnd()
        glPopMatrix()

        glColor3f(0.3, 0.3, 0.3)
        glPushMatrix()
        glTranslatef(-11, 1, 0)
        barrier_left.draw()
        glPopMatrix()

        glColor3f(0.3, 0.3, 0.3)
        glPushMatrix()
        glTranslatef(11, 1, 0)
        barrier_right.draw()
        glPopMatrix()

        for zombie in zombieList:
            glPushMatrix()
            zombie.draw(time)
            glPopMatrix()

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

        glPushMatrix()
        bob.move(leftFlag, rightFlag, spaceFlag)
        bob.draw(time)
        glPopMatrix()


        for bullet in bulletList:
            glPushMatrix()
            bullet.shoot()
            bullet.draw(time)
            glPopMatrix()

        # cleanup
        for bullet in bulletList:
            if bullet.z_cord < -30:
                bulletList.remove(bullet)
            if bullet.hit:
                bulletList.remove(bullet)

        drawText([-2, 9, 0], f"Points: {totalPoints}")

        pygame.display.flip()
        pygame.time.wait(10)


main()
