#!/usr/bin/env python3
import time
from ev3dev2.motor import OUTPUT_A, OUTPUT_D
from ev3dev2.motor import MoveTank, SpeedPercent
#from FetchSensor import fetch_sensor

drive_tank = MoveTank(OUTPUT_A, OUTPUT_D)


def turn_tank():
    drive_ws = 100
    turn_degree = 500
    drive_tank.on_for_degrees(SpeedPercent(-drive_ws), SpeedPercent(drive_ws), turn_degree)