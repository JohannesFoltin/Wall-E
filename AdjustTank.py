#!/usr/bin/env python3
import time
from ev3dev2.motor import OUTPUT_A, OUTPUT_D
from ev3dev2.motor import MoveTank, SpeedPercent
from FetchSensor import fetch_sensor

drive_tank = MoveTank(OUTPUT_A, OUTPUT_D)

drive_tank.on(-10, -10)
time.sleep(1)
drive_tank.on(-50, -100)

STATE_FOLLOW_LINE = 0
STATE_TURN_ARROUND = 1
STATE_GATE = 2
STATE_PUSH_BLOCK = 3
STATE_TROW_BALL = 4
STATE_NO_LINE = 5

NORMAL_LS = (False, True, False)  # LS = LIGHT STATE
LEFT_LS = (True, True, False)
RIGHT_LS = (False, True, True)
EDGE_L_LS = (True, False, False)
EDGE_R_LS = (False, False, True)
NO_LINE_LS = (False, False, False)

NORMAL_INSIDE_WS = -10
NORMAL_OUTSIDE_WS = -20
HARD_INSIDE_WS = 0
HARD_OUTSIDE_WS = -20

DRIVE_WS = -10
NO_LINE_WS = -3

MARK_DEGREE = -100
MAX_DEGREE = -360
MAX_BACKWARD = -1400


def handle_no_line(values_threshold):
    drive_tank.on(SpeedPercent(NO_LINE_WS), SpeedPercent(NO_LINE_WS))

    while True:
        currentStateColor = fetch_sensor(values_threshold)
        start_pos_left = drive_tank.left_motor.position

        degree = abs(drive_tank.left_motor.position - start_pos_left)

        if currentStateColor != NO_LINE_LS:
            drive_tank.stop()
            if degree < MARK_DEGREE:
                # mark start
                print('mark')
                return STATE_PUSH_BLOCK
            else:
                return STATE_FOLLOW_LINE

        elif degree > MAX_DEGREE:
            drive_tank.stop()
            start_pos_left = drive_tank.left_motor.position
            while fetch_sensor(values_threshold) == NO_LINE_LS:
                # drive back und / oder dreh 360° ob ne linie gefunden wird
                drive_tank.on(SpeedPercent(-DRIVE_WS), SpeedPercent(-DRIVE_WS))
                if abs(drive_tank.left_motor.position - start_pos_left) > MAX_BACKWARD:
                    return STATE_NO_LINE


def adjust_tank(currentStateColor, values_threshold):
    if currentStateColor == NORMAL_LS:
        drive_tank.on(SpeedPercent(DRIVE_WS), SpeedPercent(DRIVE_WS))
        print('normal')
    elif currentStateColor == LEFT_LS:
        print('left')
        drive_tank.on(SpeedPercent(NORMAL_INSIDE_WS), SpeedPercent(NORMAL_OUTSIDE_WS))
    elif currentStateColor == RIGHT_LS:
        print('right')
        drive_tank.on(SpeedPercent(NORMAL_OUTSIDE_WS), SpeedPercent(NORMAL_INSIDE_WS))
    elif currentStateColor == EDGE_L_LS:
        print('hard left')
        drive_tank.on(SpeedPercent(HARD_INSIDE_WS), SpeedPercent(HARD_OUTSIDE_WS))
    elif currentStateColor == EDGE_R_LS:
        print('hard right')
        drive_tank.on(SpeedPercent(HARD_OUTSIDE_WS), SpeedPercent(HARD_INSIDE_WS))
    elif currentStateColor == NO_LINE_LS:
        print('no line')
        handle_no_line(values_threshold)
        return STATE_NO_LINE

    return STATE_FOLLOW_LINE
