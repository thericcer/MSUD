import curses
import time
from commclass import Controller


#Control Variables
serialPort = "/dev/ttyACM0"
mode = "Drive"
direction = ['F', 'F']
motor = 'B'
steer = [90,90, 90, 90]
steerTrim = [0, 0, 0, 0]
linked = 0
speed = [0, 0]
angle = 0
readSensors = 0
sensors = [0, 0, 0, 0]
controller = Controller(serialPort, 9600, 1)
pusher='S'
lifter='S'
hook='D'
cameraBoomL=130
cameraBoomU=130
char="0"

try:


    #Screen init stuff
    stdscr = curses.initscr()
    curses.noecho()
    curses.curs_set(0)
    curses.cbreak()
    stdscr.keypad(1)
    stdscr.addstr("Robot Control")
    stdscr.timeout(10)
    stdscr.refresh()
    speedscr = curses.newwin(10, 20, 1, 0)
    steerscr = curses.newwin(10, 20, 1, 20)
    sensorscr = curses.newwin(10, 20, 1, 40)
    statusscr = curses.newwin(6, 60, 11, 0)
    mechscr=curses.newwin(7,60,17,0)
    legendscr=curses.newwin(35,50,1,61)
    speedscr.keypad(1)
    steerscr.keypad(1)
    statusscr.keypad(1)
    sensorscr.keypad(1)
    mechscr.keypad(1)
    speedscr.box()
    steerscr.box()
    statusscr.box()
    sensorscr.box()
    mechscr.box()
    legendscr.box()

    speedscr.addstr(1, 1, "Speed R: " + str(speed[0]))
    speedscr.addstr(2, 1, "Speed L: " + str(speed[1]))
    speedscr.addstr(3, 1, "Direction R: " + direction[0])
    speedscr.addstr(4, 1, "Direction L: " + direction[1])
    speedscr.addstr(5, 1, "Motor: " + motor)

    steerscr.addstr(1, 1, "Angle: " + str(angle))
    steerscr.addstr(2, 1, "Front R: " + str(steer[0]))
    steerscr.addstr(3, 1, "Front L: " + str(steer[1]))
    steerscr.addstr(4, 1, "Rear R: " + str(steer[2]))
    steerscr.addstr(5, 1, "Rear L: " + str(steer[3]))

    sensorscr.addstr(1, 1, "Sensor 1: " + str(0))
    sensorscr.addstr(2, 1, "Sensor 2: " + str(0))
    sensorscr.addstr(3, 1, "Sensor 3: " + str(0))
    sensorscr.addstr(4, 1, "Sensor 4: " + str(0))

    statusscr.addstr(1, 1, "Mode: " + mode)
    statusscr.addstr(2, 1, "Steering Not Linked")
    if controller.connected:
        statusscr.addstr(3, 1, "Microcontroller connected on: " + serialPort)
    else:
        statusscr.addstr(3, 1, "Microcontroller failed to connect on: " + serialPort + "!")
    statusscr.addstr(4, 1, "Current Status Byte: " + str(controller.statusByte))

    mechscr.addstr(1,1,"Pusher: "+ pusher)
    mechscr.addstr(2,1,"Lifter: "+ lifter)
    mechscr.addstr(3,1,"Hook: " + hook)
    mechscr.addstr(4,1,"Camera Boom Lower: "+str(cameraBoomL))
    mechscr.addstr(5,1,"Camera Boom Upper: "+str(cameraBoomU))

    legendscr.addstr(1,1,"----DRIVE MODE----")
    legendscr.addstr(2,1,"Enable Drive Mode = D")
    legendscr.addstr(3,1,"Drive Right Motors = R")
    legendscr.addstr(4,1,"Drive Left  Motors = L")
    legendscr.addstr(5,1,"Drive Both Motors = B")
    legendscr.addstr(6,1,"----------------------")
   
    legendscr.addstr(7,1,"----STEERING MODE----")
    legendscr.addstr(8,1,"Enable Steer Mode = S")
    legendscr.addstr(9,1,"Links Steering = L")
    legendscr.addstr(10,1,"----------------------")

    legendscr.addstr(11,1,"----PERIPHERAL MODE----")
    legendscr.addstr(12,1,"Platform Up = Shift-Q")
    legendscr.addstr(13,1,"Platform Stop = Shift-A")
    legendscr.addstr(14,1,"Platform Down = Shift-Z")
    legendscr.addstr(15,1,"Pusher Forward = Shift-W")
    legendscr.addstr(16,1,"Pusher Stop = Shift-S")
    legendscr.addstr(17,1,"Pusher Reverse = Shift-X")
    legendscr.addstr(18,1,"Hook Up = Shift-E")
    legendscr.addstr(19,1,"Hook Middle = Shift-D")
    legendscr.addstr(20,1,"Hook Down = Shift-C")
    legendscr.addstr(21,1,"----------------------")

    legendscr.addstr(22,1,"----ALL MODES----")
    legendscr.addstr(23,1,"Speed Up = Up Arrow")
    legendscr.addstr(24,1,"Speed Up = Down Arrow")
    legendscr.addstr(25,1,"Decrease Angle = Left Arrow")
    legendscr.addstr(26,1,"Increase Angle = Right Arrow")
    
    legendscr.addstr(27,1,"Kills Everything and resets to home = X")
    legendscr.addstr(28,1,"Turns On The Sensors (SLOW) = Z")
    legendscr.addstr(29,1,"----------------------")

    statusscr.refresh()
    speedscr.refresh()
    steerscr.refresh()
    sensorscr.refresh()
    mechscr.refresh()
    legendscr.refresh()
    #Main Loop
    while True:
        #Catch key input
        char = stdscr.getch()
        
        if char == 98:
            motor = 'B'
        elif char == 108:
            if mode == "Steer":
                linked = not linked
            else:
                motor = 'L'
        elif char == 114:
            motor = 'R'
        elif char == 100:
            mode = "Drive"
        elif char == 115:
            mode = "Steer"

        elif char == curses.KEY_UP:
            if motor == 'B':
                speed[0] += 5
                speed[1] += 5
            elif motor == 'L':
                speed[1] += 5
            elif motor == 'R':
                speed[0] += 5
        
        elif char == curses.KEY_DOWN:
            if motor == 'B':
                speed[0] -= 5
                speed[1] -= 5
            elif motor == 'L':
                speed[1] -= 5
            elif motor == 'R':
                speed[0] -= 5
                
        elif char == 120:
            curses.flash()
            speed[0] = 0
            speed[1] = 0
            steer[0] = 90 + steerTrim[0]
            steer[1] = 90 + steerTrim[1]
            steer[2] = 90 + steerTrim[2]
            steer[3] = 90 + steerTrim[3]
            angle = 0
            readSensors = 0
            lifter='S'
            pusher='S'

        elif char == 122:
            readSensors = not readSensors

        elif char == curses.KEY_LEFT:
            angle -= 5
            if linked:
                steer[0] -= 5
                steer[1] -= 5
                steer[2] -= 5
                steer[3] -= 5
            else:
                steer[0] += 5
                steer[1] -= 5
                steer[2] += 5
                steer[3] -= 5
        elif char == curses.KEY_RIGHT:
            angle += 5
            if linked:
                steer[0] += 5
                steer[1] += 5
                steer[2] += 5
                steer[3] += 5
            else:
                steer[0] -= 5
                steer[1] += 5
                steer[2] -= 5
                steer[3] += 5

        elif char==81:
            lifter='U'
        elif char==65:
            lifter='S'
        elif char==90:
            lifter='D'
        elif char==87:
            pusher='F'
        elif char==83:
            pusher='S'
        elif char==88:
            pusher='R'
	elif char==69:
	    controller.hook(0)
	    hook='U'
	elif char==68:
	    controller.hook(90)
	    hook='M'
	elif char==67:
	    controller.hook(170)
	    hook='D'

        elif char==66:
            controller.breakout()

        #Change Motor Direction
        if speed[0] >= 0:
            direction[0] = 'F'
        else:
            direction[0] = 'R'
        if speed[1] >= 0:
            direction[1] = 'F'
        else:
            direction[1] = 'R'
        #Check Motor value
        if speed[0] > 255:
            speed[0] = 255
        if speed[0] < -255:
            speed[0] = -255
        if speed[1] > 255:
            speed[1] = 255
        if speed[1] < -255:
            speed[1] = -255

        #Check Steering Values
        if angle > 90:
            angle = 90
        if angle < -90:
            angle = -90

        if steer[0] > 180:
            steer[0] = 180
        if steer[0] < 0:
            steer[0] = 0
        if steer[1] > 180:
            steer[1] = 180
        if steer[1] < 0:
            steer[1] = 0
        if steer[2] > 180:
            steer[2] = 180
        if steer[2] < 0:
            steer[2] = 0
        if steer[3] > 180:
            steer[3] = 180
        if steer[3] < 0:
            steer[3] = 0

        #Update Microcontroller and check status byte.
        if controller.connected:
            controller.writeDrivePacket('D', abs(speed[0]), abs(speed[1]), direction[0], direction[1])
            controller.writeSteerPacket('S', abs(steer[0]), abs(steer[1]), abs(steer[2]), abs(steer[3]))
            controller.pusher(pusher)
            controller.lifter(lifter)
#        if controller.statusByte[0] == 3:
#            speed[0] = 0
#            speed[1] = 0

        #Get sensor values
        if readSensors:
            controller.getSensor(0)
            sensors[0] = controller.currentSensor
            controller.getSensor(1)
            sensors[1] = controller.currentSensor
            controller.getSensor(2)
            sensors[2] = controller.currentSensor
            controller.getSensor(3)
            sensors[3] = controller.currentSensor

        #Update Display
        speedscr.erase()
        speedscr.addstr(1, 1, "Speed R: " + str(speed[0]))
        speedscr.addstr(2, 1, "Speed L: " + str(speed[1]))
        speedscr.addstr(3, 1, "Direction R: " + direction[0])
        speedscr.addstr(4, 1, "Direction L: " + direction[1])
        speedscr.addstr(5, 1, "Motor: " + motor)
        speedscr.box()
        speedscr.refresh()

        steerscr.erase()
        steerscr.addstr(1, 1, "Angle: " + str(angle))
        steerscr.addstr(2, 1, "Front R: " + str(steer[0]))
        steerscr.addstr(3, 1, "Front L: " + str(steer[1]))
        steerscr.addstr(4, 1, "Rear R: " + str(steer[2]))
        steerscr.addstr(5, 1, "Rear L: " + str(steer[3]))
        steerscr.box()
        steerscr.refresh()
        
        statusscr.clear()
        statusscr.box()
        statusscr.addstr(1, 1, "Mode: " + mode)
        if linked:
            statusscr.addstr(2, 1, "Steering Linked")
        else:
            statusscr.addstr(2, 1, "Steering Not Linked")

        if readSensors:
            statusscr.addstr(1, 45, "Sensors On")
        else:
            statusscr.addstr(1, 45, "Sensors Off")

        if controller.connected:
            statusscr.addstr(3, 1, "Microcontroller Connected on: " + serialPort)
        else:
            statusscr.addstr(3, 1, "Microcontroller failed to connect on: " + serialPort + "!")
        if controller.connected:
            statusscr.addstr(4, 1, "Current Status Byte: " + str(controller.statusByte[0]))
            if controller.statusByte[0] == 2:
                statusscr.addstr(2, 45, "OK")
            elif controller.statusByte[0] == 1:
                statusscr.addstr(2, 45, "ERROR")
        statusscr.refresh()

        sensorscr.erase()
        sensorscr.box()
        sensorscr.addstr(1, 1, "Sensor 1: " + str(sensors[0]))
        sensorscr.addstr(2, 1, "Sensor 2: " + str(sensors[1]))
        sensorscr.addstr(3, 1, "Sensor 3: " + str(sensors[2]))
        sensorscr.addstr(4, 1, "Sensor 4: " + str(sensors[3]))
        sensorscr.refresh()

        mechscr.erase()
        mechscr.box()
        mechscr.addstr(1,1,"Pusher: "+ pusher)
        mechscr.addstr(2,1,"Lifter: "+ lifter)
	mechscr.addstr(3,1,"Hook: "+ hook)
        mechscr.addstr(4,1,"Camera Boom Lower: "+str(cameraBoomL))
        mechscr.addstr(5,1,"Camera Boom Upper: "+str(cameraBoomU))
        mechscr.refresh()
        
except KeyboardInterrupt:
    stdscr.erase()
    stdscr.addstr(0, 0, "Resetting All Values to 0: ")
    stdscr.refresh()
    speed[0] = 0
    speed[1] = 0
    steer[0] = 90
    steer[1] = 90
    steer[2] = 90
    steer[3] = 90

    if controller.connected:
        controller.writeDrivePacket('D', abs(speed[0]), abs(speed[1]), direction[0], direction[1])
        controller.writeSteerPacket('S', abs(steer[0]), abs(steer[1]), abs(steer[2]), abs(steer[3]))
        stdscr.addstr("Did it")
        stdscr.refresh()


    stdscr.addstr(1, 0, "Closing Serial Port: " + serialPort)
    stdscr.refresh()
    controller.close()
    time.sleep(2)

    curses.nocbreak()
    curses.echo()
    stdscr.keypad(0)
    curses.curs_set(1)
    curses.endwin()
