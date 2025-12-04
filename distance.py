#!/usr/bin/env python3
import time
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, OUTPUT_B
from ev3dev2.motor import LargeMotor, SpeedPercent, MediumMotor
from math import cos


from ev3dev2.motor import MoveTank, SpeedPercent

drive_tank = MoveTank(OUTPUT_A, OUTPUT_D)
uss_distance = UltrasonicSensor(INPUT_1)
ball_motor = MediumMotor(OUTPUT_B)

DRIVE_SPEED = -100
TURN_DEGREE = 15

"""vor Schranke (20 cm zum Ballfänger) 14cm distance stoppen [abstand zwischen sensor und ballfänger-mittelpunkt 6cm]
if distance > 20:
    langsam fahren(aber line follow)
if distance < 13:
    langsam rückwärtsfahren
if 15 <= distance >= 13:
    stoppen
    if distance > 20:
        line follow"""

def fetch_distance():
    return uss_distance.distance_centimeters

def pick_up_ball():
    if fetch_distance() < 20:
        # langsam nach vorne
        drive_tank.on_for_degrees(SpeedPercent(DRIVE_SPEED), SpeedPercent(DRIVE_SPEED), TURN_DEGREE)
    if fetch_distance() < 13:
        # langsam rückwärts fahren
        drive_tank.on_for_degrees(SpeedPercent(DRIVE_SPEED), SpeedPercent(DRIVE_SPEED), TURN_DEGREE)
    if 13 <= fetch_distance() <= 15:
        # stoppen und warten
        drive_tank.on_for_degrees(SpeedPercent(DRIVE_SPEED), SpeedPercent(DRIVE_SPEED), TURN_DEGREE)
        if fetch_distance() > 20:
            # Ball ist im Korb wieder gradeaus
            # Drive motor off bzw line following
    


        
def push_the_block():
    #if rechts abgebogen und 
    if distance_cm < 7: 
        drive_motor.on(SpeedPercent(3)) # roboter nährt sich langsam dem block an
        if distance_cm > 20: # wenn der abstand wieder größer ist, ist der block weg
            # Rückwärts fahren und rechts kurve zurück 


def drop_the_ball():
    # if letzter abschnitt.
    if distance_cm < 7:  # langsames annähren an den korb
        drive_motor.on(SpeedPercent(3))
        if distance_cm < 2: # roboter steht kurz vor dem block
            dirve_motor.off # Motor aus und die Ball wurf mechanik aktivieren
            ball_motor.on_for_degrees(SpeedPercent(5), -90)  # - geht nach vorne
            ball_motor.off


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
