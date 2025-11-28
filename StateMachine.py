#!/usr/bin/env python3
import time
from AdjustTank import adjust_tank
from FetchSensor import fetch_sensor, init_threshold, update_threshold
from TurnTank import turn_tank
# from BlockPush import push_block
from ev3dev2.motor import OUTPUT_A, OUTPUT_D
from ev3dev2.motor import MoveTank, SpeedPercent

drive_tank = MoveTank(OUTPUT_A, OUTPUT_D)

STATE_FOLLOW_LINE = 0
STATE_TURN_ARROUND = 1
STATE_GATE = 2
STATE_PUSH_BLOCK = 3
STATE_TROW_BALL = 4
current_state = STATE_FOLLOW_LINE


def State_machine():
    global current_state
    values_threshold = init_threshold()
    print(values_threshold)

    while True:
        while current_state == STATE_FOLLOW_LINE:
            values_threshold = update_threshold(values_threshold)
            print(values_threshold[0], values_threshold[1])
            current_state = adjust_tank(fetch_sensor(values_threshold), values_threshold)
            time.sleep(0.1)

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
