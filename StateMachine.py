#!/usr/bin/env python3
import time
from AdjustTank import adjust_tank, handle_no_line
from FetchSensor import fetch_sensor, init_threshold, update_threshold
from TurnTank import turn_tank
from ev3dev2.motor import OUTPUT_A, OUTPUT_D
from ev3dev2.motor import MoveTank, SpeedPercent

drive_tank = MoveTank(OUTPUT_A, OUTPUT_D)

STATE_FOLLOW_LINE = 0
STATE_TURN_ARROUND = 1
STATE_GATE = 2
STATE_PUSH_BLOCK = 3
STATE_TROW_BALL = 4
STATE_NO_LINE = 5
current_state = STATE_FOLLOW_LINE

HAS_TURNED = False
HAS_PUSHED = False
HAS_BALL = False


def State_machine():
    global current_state, HAS_TURNED, HAS_BALL, HAS_PUSHED
    values_threshold = init_threshold()
    while True:
        while current_state == STATE_FOLLOW_LINE:
            values_threshold = update_threshold(values_threshold)
            current_state = adjust_tank(fetch_sensor(values_threshold), values_threshold)
            time.sleep(0.3)

        if current_state == STATE_NO_LINE:
            if not HAS_TURNED:
                turn_tank()
                HAS_TURNED = True
            else:
                current_state = handle_no_line(values_threshold)

        if current_state == STATE_TURN_ARROUND:
            turn_tank()
            current_state = STATE_FOLLOW_LINE
        # elif current_state == STATE_GATE:
        #     pass
        # elif current_state == STATE_PUSH_BLOCK:
        #     push_block()
        #     # TODO drive_back to line
        #     current_state = STATE_FOLLOW_LINE
        # elif current_state == STATE_TROW_BALL:
        #     pass


# MAYBE TODO funktion gibt state änderung als return zurück
State_machine()
