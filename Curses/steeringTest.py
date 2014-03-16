from math import *
from commclass import Controller
import time
import curses
import struct

try:
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    
    PI = 3.14159
    length = 10.0
    width = 4.0
    radius = 0

    angle = 0
    leftAngleFront = 90
    rightAngleFront = 90
    leftAngleRear = 90
    rightAngleRear = 90

    velocity = 0
    leftVelocity = 0.0
    rightVelocity = 0.0

    controller = Controller("/dev/ttyACM0", 9600, 1)
    direction = 'F'

    while True:
        stdscr.erase()
        stdscr.addstr(0, 0, "Angle: " + str(angle) + " Velocity: " + str(velocity))
        stdscr.addstr(1, 0, "Left Angle: " + str(leftAngleFront) + " Left Velocity: " + str(leftVelocity))
        stdscr.addstr(2, 0, "Left Angle: " + str(leftAngleRear) + " Left Velocity: " + str(leftVelocity))
        stdscr.addstr(3, 0, "Right Angle: " + str(rightAngleFront) + " Right Velocity: " + str(rightVelocity))
        stdscr.addstr(4, 0, "Right Angle: " + str(rightAngleRear) + " Right Velocity: " + str(rightVelocity))
        stdscr.refresh()

        char = stdscr.getch()

        if char == curses.KEY_UP:
            velocity += 5

        if char == curses.KEY_DOWN:
            velocity -= 5

        if char == curses.KEY_RIGHT:
            angle += 1

        if char == curses.KEY_LEFT:
            angle -= 1

        if angle != 0:
            radius = length / tan(angle*(PI/180))

        
        leftAngleFront = (180/PI)*(atan(length/(radius-width))) + 90
        rightAngleFront = (180/PI)*(atan(length/(radius+width))) + 90
        leftAngleRear = 90 - (180/PI)*(atan(length/(radius-width)))
        rightAngleRear = 90 - (180/PI)*(atan(length/(radius+width)))

        leftVelocity =  velocity * (atan(length/radius-width))
        rightVelocity = velocity * (atan(length/radius+width))
            
        if leftVelocity < 0:
            leftVelocity = abs(leftVelocity)
            direction = 'R'
        else:
            direction = 'F'
        if rightVelocity < 0:
            rightVelocity = abs(rightVelocity)
            direction = 'R'
        else:
            direction = 'F'

        controller.writeDrivePacket('D', leftVelocity, rightVelocity, direction, direction)
        controller.writeSteerPacket('S', leftAngleFront, leftAngleRear, rightAngleRear, rightAngleFront)
        
except KeyboardInterrupt:
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(0)
    curses.endwin()
    controller.writeDrivePacket('D', 0, 0, 'F', 'F')
    controller.writeSteerPacket('S', 90, 90, 90, 90)
    controller.close()
