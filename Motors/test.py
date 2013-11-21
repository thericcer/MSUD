import time
import struct
import serial

port = serial.Serial("/dev/ttyACM0", baudrate = 9600, timeout = 1)

motorLspeed = 0
motorRspeed = 0



while motorLspeed < 255:
    port.write(struct.pack("<cBBcc", 'D', motorLspeed, motorRspeed, 'R', 'F'))
    motorLspeed += 15
    time.sleep(0.5)
#    if (port.read() != 'R'):
#        break
print ('first')
motorLspeed = 0;
    
while motorRspeed < 255:
    port.write(struct.pack("<cBBcc", 'D', motorLspeed, motorRspeed, 'F', 'R'))
    motorRspeed += 15
    time.sleep(0.5)
#    if (port.read() != 'R'):
#        break
print ('second')
motorRspeed = 0;

while motorLspeed < 255:
    port.write(struct.pack("<cBBcc", 'D', motorLspeed, motorLspeed, 'R', 'R'))
    motorLspeed += 15
    time.sleep(0.5)
#    if (port.read() != 'R'):
#        break
print ('third')
motorLspeed = 0

while motorLspeed < 255:
    port.write(struct.pack("<cBBcc", 'D', motorLspeed, motorLspeed, 'F', 'F'))
    motorLspeed += 15
    time.sleep(0.5)
#    if (port.read() != 'R'):
#        break
    
print('fourth')
port.write(struct.pack("<cBBcc", 'D', 255, 255, 'F', 'F'))
time.sleep(10)
port.write(struct.pack("<cBBcc", 'D', 0, 0, 'F', 'F'))
print(port.readline())

