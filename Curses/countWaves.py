from commclass import Controller
import time


serialPort = "/dev/ttyACM0"
controller = Controller(serialPort, 9600, 1)
sensors = [0, 0]
breakCount = 0
timeTillEnd = 0

try:
    if controller.connected:
        print("Robot Connected")
        time.sleep(2)
    else:
        print("Robot Failed to Connect")
        raise KeyboardInterrupt

    while True:
        controller.getSensor(2)
        sensors[0] = controller.currentSensor
        controller.getSensor(3)
        sensors[1] = controller.currentSensor
        print("Moving till Break")
        controller.writeSteerPacket('S', 90, 90, 90, 90)
        controller.writeDrivePacket('D', 130, 130, 'R', 'R')

        if sensors[0] > 1000:
            controller.writeDrivePacket('D', 0, 0, 'R', 'R')
            breakCount += 1
            print ("Found Break! " + str(breakCount))            
            time.sleep(5)
            controller.getSensor(2)
            sensors[0] = controller.currentSensor
            
            controller.writeDrivePacket('D', 255, 255, 'R', 'R')
            print("Moving Til Gap Over")
            while sensors[0] > 1000:
                controller.getSensor(2)
                sensors[0] = controller.currentSensor
            

            print("Measuring time until rear sensor drops off")

            controller.writeDrivePacket('D', 130, 130, 'R', 'R')
            controller.getSensor(3)
            sensors[1] = controller.currentSensor
            while sensors[1] < 1000:
                controller.getSensor(3)
                sensors[1] = controller.currentSensor
                time.sleep(0.1)
                timeTillEnd += 0.1

            controller.writeDrivePacket('D', 0, 0, 'R', 'R')
            print("Measured 10ths: " + str(timeTillEnd))
            timeTillEnd = 0
            time.sleep(5)
                    


except KeyboardInterrupt:
    print("Closing")
    controller.writeDrivePacket('D', 0, 0, 'F', 'F')
    controller.close()
