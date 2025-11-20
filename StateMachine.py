#!/usr/bin/env python3
import time
from AdjustWheels import adjust_wheels
from FetchSensor import fetch_sensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B
from ev3dev2.motor import LargeMotor, SpeedPercent

control_motor = LargeMotor(OUTPUT_A)
drive_motor = LargeMotor(OUTPUT_B)
STATE_FOLLOW_LINE = 0
current_state = STATE_FOLLOW_LINE
currentAngle = 0  # Links: -200 Rechts: +200


def State_machine():
    global current_state, STATE_FOLLOW_LINE, currentAngle
    drive_motor.on(SpeedPercent(-10))
    while current_state == STATE_FOLLOW_LINE:
        print('adjust_wheels')
        print(currentAngle)
        currentAngle = adjust_wheels(fetch_sensor, currentAngle)
        time.sleep(0.3)


State_machine()
