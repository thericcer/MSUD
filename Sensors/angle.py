import math
import struct
import serial
import time
try:
    port = serial.Serial("/dev/ttyACM0", baudrate = 9600, timeout = 1)
    sensorData = ""
    Command = 0
    Ultrasonic = 0
    Ultrasonic2 = 0
    Angle = 0
    print("Waiting for reset?????")
    time.sleep(5)
    
    while 1:
        port.write(struct.pack("<cBBcc", "Z", 0, 1, "F", "F"))
        sensorData = port.read(3);
        if (len(sensorData) == 3):
            Command = struct.unpack("<BH", sensorData)
            Ultrasonic = Command[1]
        else:
            print("Read Error Ultrasonic")
            
            
            
            
        port.write(struct.pack("<cBBcc", "Z", 1, 1, "F", "F"))
        sensorData = port.read(3);
        if (len(sensorData) == 3):
            Command = struct.unpack("<BH", sensorData)
            Ultrasonic2 = Command[1]
        else:
            print("Read Error")
                
           
        Angle = math.atan2(Ultrasonic-Ultrasonic2, 500)
#        print "Angle: {}".format(Angle)
        if(abs(Angle) < 0.3):
            print("Parallel")
        elif(Angle < -0.3):
            print("Front Away")
        else:
            print("Back Away")


except KeyboardInterrupt:
    port.close()
    print "Serial Port Closed, Program Finished"

