#!/usr/bin/env python3
import time
from ev3dev2.motor import OUTPUT_A, OUTPUT_D
from ev3dev2.motor import MoveTank, SpeedPercent
from FetchSensor import fetch_sensor

drive_tank = MoveTank(OUTPUT_A, OUTPUT_D)

drive_tank.on(100, 100)
time.sleep(1)
drive_tank.on(50, 100)

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

MARK_DEGREE = 100
MAX_DEGREE = 360
MAX_BACKWARD = 1400


def turn_tank(turn_direction, values_threshold):
    # maybe add timeout     start_time = time.time()        if time.time() - start_time > timeout:            break  
    if turn_direction == 'left':
        while fetch_sensor(values_threshold) != NORMAL_LS:
            drive_tank.on(SpeedPercent(NORMAL_INSIDE_WS), SpeedPercent(NORMAL_OUTSIDE_WS))
            time.sleep(0.3)

    elif turn_direction == 'hard_left':
        while fetch_sensor(values_threshold) != NORMAL_LS:
            drive_tank.on(SpeedPercent(HARD_INSIDE_WS), SpeedPercent(HARD_OUTSIDE_WS))
            time.sleep(0.3)

    elif turn_direction == 'right':
        while fetch_sensor(values_threshold) != NORMAL_LS:
            drive_tank.on(SpeedPercent(NORMAL_OUTSIDE_WS), SpeedPercent(NORMAL_INSIDE_WS))
            time.sleep(0.3)

    elif turn_direction == 'hard_right':
        while fetch_sensor(values_threshold) != NORMAL_LS:
            drive_tank.on(SpeedPercent(HARD_OUTSIDE_WS), SpeedPercent(HARD_INSIDE_WS))
            time.sleep(0.3)


def handle_no_line(values_threshold):
    while True:
        no_line_speed = SpeedPercent(20)
        drive_tank.on(no_line_speed, no_line_speed)

        currentStateColor = fetch_sensor(values_threshold)
        start_pos_left = drive_tank.left_motor.position        

        degree = abs(drive_tank.left_motor.position - start_pos_left)
        drive_tank.on(SpeedPercent(NO_LINE_WS), SpeedPercent(NO_LINE_WS))
 
        if currentStateColor != NO_LINE_LS:
            drive_tank.stop()
            if degree < MARK_DEGREE:
                #mark start
                print('mark')
                return
            else:
                return
            
        elif degree > MAX_DEGREE:
            drive_tank.stop()
            start_pos_left = drive_tank.left_motor.position
            while fetch_sensor(values_threshold) == NO_LINE_LS:
                # drive back und / oder dreh 360° ob ne linie gefunden wird
                drive_tank.on(SpeedPercent(-DRIVE_WS), SpeedPercent(-DRIVE_WS))
                if abs(drive_tank.left_motor.position - start_pos_left) > MAX_BACKWARD:
                    return
        return


def adjust_tank(currentStateColor, values_threshold):
    if currentStateColor == NORMAL_LS:
        print('normal')
    elif currentStateColor == LEFT_LS:
        print('left')
        turn_tank('left', values_threshold)
    elif currentStateColor == RIGHT_LS:
        print('right')
        turn_tank('right', values_threshold)
    elif currentStateColor == EDGE_L_LS:
        print('hard left')
        turn_tank('hard_left', values_threshold)
    elif currentStateColor == EDGE_R_LS:
        print('hard right')
        turn_tank('hard_right', values_threshold)
    elif currentStateColor == NO_LINE_LS:
        print('no line')
        handle_no_line(values_threshold)
    return
