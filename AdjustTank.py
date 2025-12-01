#!/usr/bin/env python3
import time
from ev3dev2.motor import OUTPUT_A, OUTPUT_D
from ev3dev2.motor import MoveTank, SpeedPercent
from FetchSensor import fetch_sensor

drive_tank = MoveTank(OUTPUT_A, OUTPUT_D)

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

DRIVE_SPEED = -10
HALF_DRIVE_SPEED = 0.5 * DRIVE_SPEED
NO_LINE_SPEED = DRIVE_SPEED - 8

MARK_DEGREE = -100
MAX_DEGREE = -360
MAX_BACKWARD = -1400


def handle_no_line(values_threshold):
    drive_tank.on(SpeedPercent(NO_LINE_SPEED), SpeedPercent(NO_LINE_SPEED))
    start_pos_left = drive_tank.left_motor.position
    while True:
        currentStateColor = fetch_sensor(values_threshold)
        degree = abs(drive_tank.left_motor.position - start_pos_left)

        if currentStateColor != NO_LINE_LS:
            drive_tank.stop()
            degree = abs(drive_tank.left_motor.position - start_pos_left)
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
                drive_tank.on(SpeedPercent(-DRIVE_SPEED), SpeedPercent(-DRIVE_SPEED))
                if abs(drive_tank.left_motor.position - start_pos_left) > MAX_BACKWARD:
                    return STATE_NO_LINE


def adjust_tank(currentStateColor, values_threshold):
    if currentStateColor == NORMAL_LS:
        drive_tank.on(SpeedPercent(DRIVE_SPEED), SpeedPercent(DRIVE_SPEED))
        print('normal')
    elif currentStateColor == LEFT_LS:
        print('left')
        drive_tank.on(SpeedPercent(DRIVE_SPEED), SpeedPercent(-HALF_DRIVE_SPEED))
    elif currentStateColor == RIGHT_LS:
        print('right')
        drive_tank.on(SpeedPercent(-HALF_DRIVE_SPEED), SpeedPercent(DRIVE_SPEED))
    elif currentStateColor == EDGE_L_LS:
        print('hard left')
        drive_tank.on(SpeedPercent(DRIVE_SPEED), SpeedPercent(-HALF_DRIVE_SPEED))
    elif currentStateColor == EDGE_R_LS:
        print('hard right')
        drive_tank.on(SpeedPercent(-HALF_DRIVE_SPEED), SpeedPercent(DRIVE_SPEED))
    elif currentStateColor == NO_LINE_LS:
        print('no line')
        drive_tank.on(SpeedPercent(DRIVE_SPEED), SpeedPercent(DRIVE_SPEED))
        #handle_no_line(values_threshold)
        #return STATE_NO_LINE

    return STATE_FOLLOW_LINE
