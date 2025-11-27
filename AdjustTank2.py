#!/usr/bin/env python3
import time
from ev3dev2.motor import OUTPUT_A, OUTPUT_B
from ev3dev2.motor import MoveTank#, SpeedPercent
#from FetchSensor import fetch_sensor

drive_tank = MoveTank(OUTPUT_A, OUTPUT_B)

drive_tank.on(100, 100)
time.sleep(1)
drive_tank.on(50, 100)


'''
NORMAL_LS = (False, True, False)  # LS = LIGHT STATE
LEFT_LS = (True, True, False)
RIGHT_LS = (False, True, True)
EDGE_L_LS = (True, False, False)
EDGE_R_LS = (False, False, True)
NO_LINE_LS = (False, False, False)

NORMAL_INSIDE_WS = 50
NORMAL_OUTSIDE_WS = 70
HARD_INSIDE_WS = 0
HARD_OUTSIDE_WS = 70

DRIVE_WS = 100
NO_LINE_WS = 30


def turn_tank(turn_direction, values_threshold):
    # maybe add timeout     start_time = time.time()        if time.time() - start_time > timeout:            break  
    if turn_direction == 'left':
        while fetch_sensor(values_threshold) != NORMAL_LS:
            drive_tank.on(SpeedPercent(NORMAL_INSIDE_WS), SpeedPercent(NORMAL_OUTSIDE_WS))

    elif turn_direction == 'hard_left':
        while fetch_sensor(values_threshold) != NORMAL_LS:
            drive_tank.on(SpeedPercent(HARD_INSIDE_WS), SpeedPercent(HARD_OUTSIDE_WS))

    elif turn_direction == 'right':
        while fetch_sensor(values_threshold) != NORMAL_LS:
            drive_tank.on(SpeedPercent(NORMAL_OUTSIDE_WS), SpeedPercent(NORMAL_INSIDE_WS))

    elif turn_direction == 'hard_right':
        while fetch_sensor(values_threshold) != NORMAL_LS:
            drive_tank.on(SpeedPercent(HARD_OUTSIDE_WS), SpeedPercent(HARD_INSIDE_WS))


def handle_no_line(values_threshold):
    global NORMAL_INSIDE_WS, NORMAL_OUTSIDE_WS, NORMAL_OUTSIDE_WS
    while True:
        currentStateColor = fetch_sensor(values_threshold)
        start_pos_left = drive_tank.left_motor.position
        start_pos_right = drive_tank.right_motor.position
        
        max_rotations = 360
        rotations = abs(drive_tank.left_motor.position - start_pos_left)
        drive_tank.on(SpeedPercent(NO_LINE_WS), SpeedPercent(NO_LINE_WS))

        if currentStateColor != NO_LINE_LS:
            drive_tank.stop()
            if rotations < max_rotations:
                return
            
        elif rotations > max_rotations:
            drive_tank.stop()
            while fetch_sensor(values_threshold) == NO_LINE_LS:
                # drive back 
                drive_tank.on(SpeedPercent(-DRIVE_WS), SpeedPercent(-DRIVE_WS))
                return

def adjust_tank(currentStateColor, values_threshold):
    if currentStateColor == NORMAL_LS:
        return
    elif currentStateColor == LEFT_LS:
        turn_tank('left', values_threshold)
    elif currentStateColor == RIGHT_LS:
        turn_tank('right', values_threshold)
    elif currentStateColor == EDGE_L_LS:
        turn_tank('hard_left', values_threshold)
    elif currentStateColor == EDGE_R_LS:
        turn_tank('hard_right', values_threshold)
    elif currentStateColor == NO_LINE_LS:
        handle_no_line(values_threshold)
'''
