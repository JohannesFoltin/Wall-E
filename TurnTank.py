#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_D
from ev3dev2.motor import MoveTank, SpeedPercent

drive_tank = MoveTank(OUTPUT_A, OUTPUT_D)


# Führt eine 180° Drehung des Roboters durch.
def turn_tank():
    TURN_WS = 30  # Drehgeschwindigkeit
    TURN_DEGREE = 420  # Drehgrad für 180° Drehung
    # Drehe den Roboter um 180 Grad
    drive_tank.on_for_degrees(SpeedPercent(-TURN_WS), SpeedPercent(TURN_WS), TURN_DEGREE)
