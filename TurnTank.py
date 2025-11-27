#!/usr/bin/env python3
import time
from ev3dev2.motor import OUTPUT_A, OUTPUT_D
from ev3dev2.motor import MoveTank, SpeedPercent
#from FetchSensor import fetch_sensor

drive_tank = MoveTank(OUTPUT_A, OUTPUT_D)


def turn_tank():
    DRIVE_WS = 100
    TURN_DEGREE = 500
    drive_tank.on_for_degrees(SpeedPercent(-DRIVE_WS), SpeedPercent(DRIVE_WS), TURN_DEGREE)