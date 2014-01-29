from commclass import Controller
import time
import serial
import math

serialPort = "/dev/ttyACM0"
controller = Controller(serialPort, 9600, 1)
sensors = [0, 0, 0, 0]
angle = 0
parallel = 0
distance = 0

def setDistance(maximum, minimum):
    controller.getSensor(0)
    current = controller.currentSensor

    if current < minimum:
        print("Going Toward!")
        while current < minimum:
            controller.getSensor(0)
            current = controller.currentSensor
            controller.writeSteerPacket('S', 0, 0, 0, 0)
            controller.writeDrivePacket('D', 130, 130, 'R', 'R')
            
    elif current > maximum:
        print("Going Away!")
        while current > maximum:
            controller.getSensor(0)
            current = controller.currentSensor
            controller.writeSteerPacket('S', 0, 0, 0, 0)
            controller.writeDrivePacket('D', 130, 130, 'F', 'F')

    
    controller.writeDrivePacket('D', 0, 0, 'F', 'F')
    controller.writeSteerPacket('S', 90, 90, 90, 90)

def getParallel():

    parallel = 0
    while parallel == 0:
        controller.getSensor(0)
        sensors[0] = controller.currentSensor
        controller.getSensor(1)
        sensors[1] = controller.currentSensor
        angle = math.atan2((sensors[0]-sensors[1]), 480)

        if angle < -0.05:
            controller.writeSteerPacket('S', 135, 45, 45, 135)
            controller.writeDrivePacket('D', 255, 255, 'R', 'F')
            

        elif angle > 0.05:
             controller.writeSteerPacket('S', 135, 45, 45, 135)
             controller.writeDrivePacket('D', 255, 255, 'F', 'R')
             

        else:
            controller.writeSteerPacket('S', 90, 90, 90, 90)
            controller.writeDrivePacket('D', 0, 0, 'F', 'F')
            parallel = 1
            return parallel
            
def driveTime(speed, direction, duration):
    controller.writeDrivePacket('D', speed, speed, direction, direction)
    time.sleep(duration)
    controller.writeDrivePacket('D', 0, 0, 'F', 'F')


try:
    if controller.connected:
        print("Controller Connected!")
    else:
        print("Controller Failed to Connect!")
        raise KeyboardInterrupt
    forward = 1

    while True:
        
        print("Rear: " + str(sensors[0]) + " Front: " + str(sensors[1]) + " Angle: " + str(angle) + " Parallel: " + str(parallel))

        
        setDistance(500, 300)

        time.sleep(1)
        
        parallel = getParallel()

        time.sleep(1)

        if parallel:
            if forward:
                driveTime(255, 'F', 5)
                forward = not forward
            else:
                driveTime(255, 'R', 5)
                forward = not forward

except KeyboardInterrupt:
    controller.writeDrivePacket('D', 0, 0, 'F', 'F')
    controller.writeSteerPacket('S', 90, 90, 90, 90)
    controller.close()
    print("Serial Port Closed!")
