#!/usr/bin/env python3
import time
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import UltrasonicSensor
from math import cos

uss_distance = UltrasonicSensor(INPUT_1)
distance_cm = uss_distance.distance_centimeters


"""while i == 1:
    print(distance_cm)
    time.sleep(2)"""

#def distance(distance_cm: int) -> int:
    



"""def distance(distance_cm):
    distance = cos(0.3054326) * distance_cm
    print("hypotenuse=", distance_cm)
    return distance"""

i = 1
while i == 1:
    print(distance_cm)
    uss_distance = UltrasonicSensor(INPUT_1)
    distance_cm = uss_distance.distance_centimeters
    time.sleep(1)
