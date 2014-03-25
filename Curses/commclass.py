import struct
import serial
import time

class Controller:

    connected = 0
    currentSensor = 0

    def __init__(self,  port, baud, time):
        try:
            self.port = serial.Serial(port, baudrate = baud, timeout = time)
            self.connected = 1
            self.statusByte = 0
        except serial.SerialException:
            self.connected = 0
            self.statusByte = -1

    #Packet Structure D S1 S2 DirL DirR
    def writeDrivePacket(self, byte1, byte2, byte3, byte4, byte5):
        if self.connected:
            self.port.write(struct.pack("<cBBcc", byte1, byte2, byte3, byte4, byte5))
            data = self.port.read()
            if len(data) != 1:
                self.statusByte = -1
            else:
                self.statusByte = struct.unpack("<B", data)
        
    #Packet Structure S A1 A2 A3 A4
    def writeSteerPacket(self, byte1, byte2, byte3, byte4, byte5):
        if self.connected:
            self.port.write(struct.pack("<cBBBB", byte1, byte2, byte3, byte4, byte5))
            data = self.port.read()
            if len(data) != 1:
                self.statusByte = -1
            else:
                self.statusByte = struct.unpack("<B", data)

    #Get a sensor value and store it in currentSensor variable.
    def getSensor(self, sensor):
        if self.connected:
            self.port.write(struct.pack("<cBBcc", "Z", sensor, 1, 'F', 'F'))
            sensorData = self.port.read(3)
            if (len(sensorData) == 3):
                Command = struct.unpack("<BH", sensorData)
                self.currentSensor = Command[1]

    def pusher(self, direction):
        if self.connected:
            self.port.write(struct.pack("<ccBBB",'K',direction,0,0,0))
            data=self.port.read()
            if len(data) !=1:
                self.statusByte=-1
            else:
                self.statusByte=struct.unpack("<B",data)

    def lifter(self, direction):
        if self.connected:
            self.port.write(struct.pack("<ccBBB",'P',direction,0,0,0))
            data=self.port.read()
            if len(data) !=1:
                self.statusByte=-1
            else:
                self.statusByte=struct.unpack("<B",data)

    def close(self):
        if self.connected:
            self.port.close()

        self.connected = 0
