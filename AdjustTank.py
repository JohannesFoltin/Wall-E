#!/usr/bin/env python3
import time
from ev3dev2.motor import OUTPUT_A, OUTPUT_D
from ev3dev2.motor import MoveTank, SpeedPercent

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
ALL_BLACK = (True, True, True)
NO_LINE_LS = (False, False, False)

DRIVE_SPEED = -50
CONTINUE_SPEED = DRIVE_SPEED * 0.6
HALF_DRIVE_SPEED = 0.5 * DRIVE_SPEED
NO_LINE_SPEED = DRIVE_SPEED * 0.8
TURN_DEGREE = 10

MARK_DEGREE = -100


def turn_angle_white(last_state):
    if (last_state == LEFT_LS) or (last_state == EDGE_L_LS):
        drive_tank.on_for_degrees(SpeedPercent(HALF_DRIVE_SPEED), SpeedPercent(-HALF_DRIVE_SPEED), 4 * TURN_DEGREE)
    elif (last_state == RIGHT_LS) or (last_state == EDGE_R_LS):
        drive_tank.on_for_degrees(SpeedPercent(-HALF_DRIVE_SPEED), SpeedPercent(HALF_DRIVE_SPEED), 4 * TURN_DEGREE)


def drive_back(currentStateColor, last_state):
    if currentStateColor == NO_LINE_LS:
        if last_state == NO_LINE_LS:
            drive_tank.on(SpeedPercent(-CONTINUE_SPEED), SpeedPercent(-CONTINUE_SPEED))
        else:
            drive_tank.on_for_degrees(SpeedPercent(-DRIVE_SPEED), SpeedPercent(-DRIVE_SPEED), TURN_DEGREE)
        return STATE_NO_LINE, NO_LINE_LS
    else:
        return STATE_FOLLOW_LINE, NO_LINE_LS


def tank_stop():
    drive_tank.off()
    time.sleep(0.2)


def adjust_tank(currentStateColor, last_state):
    save_current_state = NORMAL_LS
    if currentStateColor == NORMAL_LS:
        if last_state == NORMAL_LS:
            drive_tank.on(SpeedPercent(CONTINUE_SPEED), SpeedPercent(CONTINUE_SPEED))
        else:
            drive_tank.on_for_degrees(SpeedPercent(DRIVE_SPEED), SpeedPercent(DRIVE_SPEED), TURN_DEGREE)
        save_current_state = NORMAL_LS
        print('normal')

    elif currentStateColor == LEFT_LS:
        print('left')
        drive_tank.on_for_degrees(SpeedPercent(-HALF_DRIVE_SPEED), SpeedPercent(DRIVE_SPEED), TURN_DEGREE)
        save_current_state = LEFT_LS

    elif currentStateColor == RIGHT_LS:
        print('right')
        drive_tank.on_for_degrees(SpeedPercent(DRIVE_SPEED), SpeedPercent(-HALF_DRIVE_SPEED), TURN_DEGREE)
        save_current_state = RIGHT_LS

    elif currentStateColor == EDGE_L_LS:
        print('hard left')
        drive_tank.on_for_degrees(SpeedPercent(-DRIVE_SPEED), SpeedPercent(DRIVE_SPEED), 1.5 * TURN_DEGREE)
        save_current_state = EDGE_L_LS

    elif currentStateColor == EDGE_R_LS:
        print('hard right')
        drive_tank.on_for_degrees(SpeedPercent(DRIVE_SPEED), SpeedPercent(-DRIVE_SPEED), 1.5 * TURN_DEGREE)
        save_current_state = EDGE_R_LS

    elif currentStateColor == NO_LINE_LS:
        drive_tank.on(SpeedPercent(CONTINUE_SPEED), SpeedPercent(CONTINUE_SPEED))
        print('no line')
        return STATE_NO_LINE, NO_LINE_LS

    elif currentStateColor == ALL_BLACK:
        if last_state == LEFT_LS or last_state == EDGE_L_LS:
            drive_tank.on_for_degrees(SpeedPercent(-DRIVE_SPEED), SpeedPercent(DRIVE_SPEED), 1.5 * TURN_DEGREE)
        elif last_state == RIGHT_LS or last_state == EDGE_R_LS:
            drive_tank.on_for_degrees(SpeedPercent(DRIVE_SPEED), SpeedPercent(-DRIVE_SPEED), 1.5 * TURN_DEGREE)
        else:
            drive_tank.on_for_degrees(SpeedPercent(DRIVE_SPEED), SpeedPercent(DRIVE_SPEED), TURN_DEGREE)
        save_current_state = ALL_BLACK
        print('all black')

    return STATE_FOLLOW_LINE, save_current_state
