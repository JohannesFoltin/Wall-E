#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_D
from ev3dev2.motor import MoveTank, SpeedPercent

drive_tank = MoveTank(OUTPUT_A, OUTPUT_D)


def turn_tank():
    TURN_WS = 30
    TURN_DEGREE = 350
    drive_tank.on_for_degrees(SpeedPercent(-TURN_WS), SpeedPercent(TURN_WS), TURN_DEGREE)
