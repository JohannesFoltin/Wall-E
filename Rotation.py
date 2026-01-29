#!/usr/bin/env python3
import time
from ev3dev2.motor import OUTPUT_A, OUTPUT_D
from ev3dev2.motor import MoveTank, SpeedPercent

drive_tank = MoveTank(OUTPUT_A, OUTPUT_D)

DRIVE_SPEED = -25  # Fahrgeschwindigkeit zum Korrigieren
TURN_DEGREE = 154  # Inkrement für Korrekturen
"""
i = 0
while i < 10:
    drive_tank.on_for_degrees(SpeedPercent(DRIVE_SPEED), SpeedPercent(DRIVE_SPEED), TURN_DEGREE)
    i += 0.5
    print(i)
    #time.sleep(0.5)
"""

def moved_distance(moved_degrees):
    distance_per_degree = 0.07156
    distance = distance_per_degree * moved_degrees
    print(distance)
    return distance


drive_tank.on_for_degrees(SpeedPercent(DRIVE_SPEED), SpeedPercent(DRIVE_SPEED), TURN_DEGREE)
moved_distance(TURN_DEGREE)


def drive_half_centimeter():
    needed_degress = 6.99
    drive_tank.on_for_degrees(SpeedPercent(DRIVE_SPEED), SpeedPercent(DRIVE_SPEED), needed_degress)
