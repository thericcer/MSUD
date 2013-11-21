import sys
import struct
import serial
import time

port = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=1)
joy = open('/dev/input/js1', 'r')

speedR = 0
speedL = 0
directionL = 'N'
directionR = 'N'

msg = []

while 1:
    for char in joy.read(1):
        msg += [ord(char)]
        if len(msg) == 8:
                   if msg[6] == 1:
                       if msg[4] == 1:
                           print (msg[7])
                           if msg[7] == 0:
                               directionR = 'F'
                           if msg[7] == 1:
                               directionR = 'R'

                           if msg[7] == 2:
                               directionL = 'F'
                           if msg[7] == 3:
                               directionL = 'R'
                           
                       #else:
                           #print ('Right: ', directionR, 'Left: ', directionL)

                   elif msg[6] == 2:
                       if msg[7] == 5:
                           if int(msg[5]) < 128:
                               speedR = int(msg[5])
                               #print ('Right: ', directionR, speedR)
                           else:
                               speedR = 0

                       if msg[7] == 2:
                           if int(msg[5]) < 128:
                               speedL = int(msg[5])
                              # print ('Left: ', directionL, speedL)
                           else:
                               speedL = 0
                       
                       if msg[7] == 0:
                           if int(msg[5]) > 128:
                               print ('Turn Left', 256 - msg[5])
                           else:
                               print ('Turn Right', msg[5])
                   #time.sleep(0.1)
                   msg = []
                   port.write(struct.pack("<cBBcc", 'D', speedL, speedR, directionL, directionR))
                   print('D', speedL, speedR, directionL, directionR)
                              
