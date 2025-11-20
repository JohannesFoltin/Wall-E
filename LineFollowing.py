#!/usr/bin/env python3
import time
from ev3dev2.motor import OUTPUT_A, OUTPUT_B
from ev3dev2.motor import LargeMotor, SpeedPercent

control_motor = LargeMotor(OUTPUT_A)
drive_motor = LargeMotor(OUTPUT_B)

currentAngle = 0  # Links: -200 Rechts: +200
max_turn_angle = 400

turn_arround_sleep = 0.5

NORMAL_LS = (False, True, False)  # LS = LIGHT STATE
LEFT_LS = (True, True, False)
RIGHT_LS = (False, True, True)
EDGE_L_LS = (True, False, False)
EDGE_R_LS = (False, False, True)
NO_LINE_LS = (False, False, False)

RIGHT_WS = -400  # WHEEL TURN STATE
LEFT_WS = 400
STRAIGHT_WS = 0

correction_time = 2
drive_speed = -10


def adjust_wheels(currentStateColor, currentAngle):
    global max_turn_angle, NORMAL_LS, LEFT_LS, RIGHT_LS, EDGE_L_LS, EDGE_R_LS, NO_LINE_LS, RIGHT_WS, LEFT_WS, STRAIGHT_WS, correction_time, drive_speed

    if currentAngle == RIGHT_WS:
        print("RightWS")
        if currentStateColor == RIGHT_LS:
            return currentAngle
        elif currentStateColor == NORMAL_LS:
            control_motor.on_for_degrees(SpeedPercent(100), LEFT_WS)
            currentAngle = STRAIGHT_WS
        elif currentStateColor == LEFT_LS:
            control_motor.on_for_degrees(SpeedPercent(100), 2 * LEFT_WS)
            currentAngle = LEFT_WS
        elif currentStateColor == EDGE_R_LS:
            print('Edge_Rechts')
            while currentStateColor == EDGE_R_LS:
                currentStateColor = fetch_sensor()
            if currentStateColor == NO_LINE_LS:
                print('Korregiere links zurueck')
                drive_motor.off
                time.sleep(turn_arround_sleep)  # vlt mybe eroooeeehhnn
                control_motor.on_for_degrees(SpeedPercent(100), 1.5 * LEFT_WS)

                drive_motor.on_for_seconds(SpeedPercent(-drive_speed), correction_time)
                drive_motor.off
                time.sleep(turn_arround_sleep)
                control_motor.on_for_degrees(SpeedPercent(100), 0.5 * RIGHT_WS)
                currentAngle = STRAIGHT_WS
                drive_motor.on(SpeedPercent(drive_speed))
    elif currentAngle == LEFT_WS:
        print("LeftWs")
        if currentStateColor == RIGHT_LS:
            control_motor.on_for_degrees(SpeedPercent(100), 2 * RIGHT_WS)
            # TODO
            currentAngle = RIGHT_WS
        elif currentStateColor == NORMAL_LS:
            control_motor.on_for_degrees(SpeedPercent(100), RIGHT_WS)
            currentAngle = STRAIGHT_WS
        elif currentStateColor == LEFT_LS:
            return currentAngle
        elif currentStateColor == EDGE_L_LS:
            print('Edge_Links')
            while currentStateColor == EDGE_L_LS:
                currentStateColor = fetch_sensor()
            if currentStateColor == NO_LINE_LS:
                print('Korregiere rechts zurueck')
                drive_motor.off
                time.sleep(turn_arround_sleep)
                control_motor.on_for_degrees(SpeedPercent(100), 1.5 * RIGHT_WS)

                drive_motor.on_for_seconds(SpeedPercent(-drive_speed), correction_time)
                drive_motor.off
                time.sleep(turn_arround_sleep)
                control_motor.on_for_degrees(SpeedPercent(100), 0.5 * LEFT_WS)
                currentAngle = STRAIGHT_WS
                drive_motor.on(SpeedPercent(drive_speed))
    elif currentAngle == STRAIGHT_WS:
        print("StraightWs")
        if ((currentStateColor == RIGHT_LS)
                or (currentStateColor == EDGE_R_LS)):
            control_motor.on_for_degrees(SpeedPercent(100), RIGHT_WS)
            # TODO
            currentAngle = RIGHT_WS
        elif currentStateColor == NORMAL_LS:
            return currentAngle
        elif ((currentStateColor == LEFT_LS)
                or (currentStateColor == EDGE_L_LS)):
            control_motor.on_for_degrees(SpeedPercent(100), LEFT_WS)
            # TODO
            currentAngle = LEFT_WS
    return currentAngle