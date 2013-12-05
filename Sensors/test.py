import struct
import serial
import time
try:
    port = serial.Serial("/dev/ttyACM0", baudrate = 9600, timeout = 1)
    sensorData = ""
    Command = 0
    Ultrasonic = 0
    Infrared = 0
    Infrared2 = 0
    
    print("Waiting for reset?????")
    time.sleep(5)
    
    while 1:
        port.write(struct.pack("<cBBcc", "Z", 1, 1, "F", "F"))
        sensorData = port.read(3);
        if (len(sensorData) == 3):
            Command = struct.unpack("<BH", sensorData)
            Ultrasonic = (Ultrasonic + Command[1])/2
        else:
            print("Read Error Ultrasonic")
            
            
            
            
        port.write(struct.pack("<cBBcc", "Z", 0, 1, "F", "F"))
        sensorData = port.read(3);
        if (len(sensorData) == 3):
            Command = struct.unpack("<BH", sensorData)
            Infrared = (Infrared + Command[1])/2
        else:
            print("Read Error")
                
        port.write(struct.pack("<cBBcc", "Z", 2, 1, "F", "F"))
        sensorData = port.read(3);
        if (len(sensorData) == 3):
             Command = struct.unpack("<BH", sensorData)
             Infrared2 = (Infrared2 + Command[1])/2
        else:
             print("Read Error")
                 
        print "Infrared1: {}\tInfrared2: {}\tUltrasonic: {}".format(Infrared, Infrared2, Ultrasonic)
                    
        '''
                    port.write(struct.pack("<cBBBB", "S", 155, 155, 155, 155))
                    sensorData = port.read()
                    if (len(sensorData) != 1):
                    print("No Status Byte!")
                    else:
                    Command = struct.unpack("<B", sensorData)
                    if (Command[0] != 2):
                    print("Bad Status Byte! " + str(Command[0]))
                    
                    port.write(struct.pack("<cBBcc", "D", 255, 255, 'F', 'R'))
                    sensorData = port.read()
                    if (len(sensorData) != 1):
                    print("No Status Byte!")
                    else:
                    Command = struct.unpack("<B", sensorData)
                    if (Command[0] != 2):
                    print("Bad Status Byte! " + str(Command[0]))
                    
                    
                    port.write(struct.pack("<ccccc", 'C', 'd', 'd', 'd', 'd'))
                    Data = port.read(11);
                    Command = struct.unpack("<BBBccBBBBH", Data)
                    print("Motor Values: " + str(Command[1]) + str(Command[2])+ str(Command[3])+ str(Command[4])+ str(Command[5])+ str(Command[6])+ str(Command[7])+ str(Command[8]) + " Infrared: " + str(Infrared) + " Ultrasonic: " + str(Ultrasonic) + "Loop Time: " + str(Command[9]))
    
                    '''
except KeyboardInterrupt:
    port.close()
    print "Serial Port Closed, Program Finished"

