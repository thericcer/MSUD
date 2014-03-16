import serial
import struct
import time
import curses

port = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=1)


try:
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    stdscr.addstr(0, 1, "Wait for micro reset")
    ack = port.readline()
    stdscr.refresh()
    time.sleep(2)
    stdscr.addstr(1, 1, "Received: " + ack)
    stdscr.refresh()
    time.sleep(1)


    pwm = [1300, 1300]
    micro = -1
    linked = 0

    while True:
        stdscr.erase()
        stdscr.addstr(0, 1, "Platform:")
        stdscr.addstr(1, 1, "Current Value: " + str(pwm[0]) + " 2: " + str(pwm[1]))
        stdscr.addstr(2, 1, "Returned from Micro: " + str(micro))

        char = stdscr.getch()

        if char == 120:
            pwm[0] = 1300
            pwm[1] = 1300

        if char == 119:
            pwm[0] += 5
            if pwm[0] > 1700:
                pwm[0] = 1700
                
                
        if char == 115:
            pwm[0] -= 5
            if pwm[0] < 900:
                pwm[0] = 900

        if char == 105:
            pwm[1] += 5
            if pwm[1] > 1700:
                pwm[1] = 1700
        
        if char == 107:
            pwm[1] -= 5
            if pwm[1] < 900:
                pwm[1] = 900

        if char == curses.KEY_UP:
            pwm[0] += 5
            pwm[1] += 5
            if pwm[0] > 1700:
                pwm[0] = 1700
            if pwm[1] > 1700:
                pwm[1] = 1700
        if char == curses.KEY_DOWN:
            pwm[0] -= 5
            pwm[1] -= 5
            if pwm[0] < 900:
                pwm[0] = 900
            if pwm[1] < 900:
                pwm[1] = 900

        port.write(struct.pack("<hh", pwm[0], pwm[1]))


        

except KeyboardInterrupt:        
    
    port.write(struct.pack("<hh", 1300, 1300))

    port.close()

    curses.nocbreak()
    curses.noecho()
    stdscr.keypad(0)
    curses.endwin()
