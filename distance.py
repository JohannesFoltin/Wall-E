#!/usr/bin/env python3
import time
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.motor import OUTPUT_B
from ev3dev2.motor import LargeMotor, SpeedPercent
from math import cos

drive_motor = LargeMotor(OUTPUT_B)
uss_distance = UltrasonicSensor(INPUT_1)
distance_cm = uss_distance.distance_centimeters


"""vor Schranke (20 cm zum Ballfänger) 14cm distance stoppen [abstand zwischen sensor und ballfänger-mittelpunkt 6cm]
if distance > 20:
    langsam fahren(aber line follow)
if distance < 13:
    langsam rückwärtsfahren
if 15 <= distance >= 13:
    stoppen
    if distance > 20:
        line follow"""

def pick_up_ball():
    if distance_cm < 20:
        # langsam nach vorne
        drive_motor.on(SpeedPercent(3))
    if distance_cm < 13:
        # langsam rückwärts fahren
        drive_motor.on(SpeedPercent(3))
    if 13 <= distance_cm <= 15:
        # stoppen und warten
        drive_motor.off
        if distance_cm > 20:
            # Ball ist im Korb wieder gradeaus
            # Drive motor off bzw line following
    


        
        



"""vor Bolck wenn abgebogen nach rechts und Abstand kleiner als 7 bis wieder größer als 20"""
"""while i == 1:
    print(distance_cm)
    time.sleep(2)"""

#def distance(distance_cm: int) -> int:
    



"""def distance(distance_cm):
    distance = cos(0.3054326) * distance_cm
    print("hypotenuse=", distance_cm)
    return distance"""

"""i = 1
while i == 1:
    print(distance_cm)
    distance_cm = uss_distance.distance_centimeters
    time.sleep(1)"""
