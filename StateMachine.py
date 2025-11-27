#!/usr/bin/env python3
import time
from AdjustWheels import adjust_wheels
from FetchSensor import fetch_sensor, init_threshold, update_threshold
from Turn import turn
from BlockPush import push_block
from ev3dev2.motor import OUTPUT_A, OUTPUT_B
from ev3dev2.motor import LargeMotor, SpeedPercent

control_motor = LargeMotor(OUTPUT_A)
drive_motor = LargeMotor(OUTPUT_B)
STATE_FOLLOW_LINE = 0
STATE_TURN_ARROUND = 1
STATE_GATE = 2
STATE_PUSH_BLOCK = 3
STATE_TROW_BALL = 4
current_state = STATE_FOLLOW_LINE
currentAngle = 0  # Links: -200 Rechts: +200


def State_machine():
    global current_state, STATE_FOLLOW_LINE, currentAngle
    values_threshold = init_threshold()
    print(values_threshold)
    drive_motor.on(SpeedPercent(-10))
    while current_state == STATE_FOLLOW_LINE:
        print('adjust_wheels')
        print(currentAngle)
        currentAngle = adjust_wheels(fetch_sensor(values_threshold), currentAngle)
        time.sleep(0.3)

    if current_state == STATE_TURN_ARROUND:
        turn()
        current_state = STATE_FOLLOW_LINE
    elif current_state == STATE_GATE:
        pass
    elif current_state == STATE_PUSH_BLOCK:
        push_block()
        # TODO drive_back to line
        current_state = STATE_FOLLOW_LINE
    elif current_state == STATE_TROW_BALL:
        pass


# MAYBE TODO funktion gibt state änderung als return zurück
State_machine()
