from math import atan
from math import tan
from math import cos
Length = 1.5
Width = 4.0

def steer(angle, velocity):
    radius = Length / tan((angle*(3.14159)/180))

    leftAngle = atan(1.0/(radius-Width))
    rightAngle = atan(1.0/(radius+Width))

    leftVelocity = velocity - (velocity * leftAngle)
    rightVelocity = velocity - (velocity * rightAngle)
    print "Center Radius: " + str(radius)
    print "Left Angle: " + str((leftAngle*180)/3.14159) + " Velocity: " + str(leftVelocity)
    print "Right Angle: " + str((rightAngle*180)/3.14159) + " Velocity: " + str(rightVelocity)


steer(10.0, 150)
