#!/usr/bin/env python3
import time
from FetchSensor import fetch_sensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B
from ev3dev2.motor import LargeMotor, SpeedPercent

control_motor = LargeMotor(OUTPUT_A)
drive_motor = LargeMotor(OUTPUT_B)


def turn():
    # if linie weg oder abstand 20cm
    DRIVE_SPEED = -10
    TURN_SPEED = SpeedPercent(80)
    TURN_ANGLE = 300  # max turn angle
    DEGREE_TURN = 132

    control_motor.on_for_degrees(TURN_SPEED, -TURN_ANGLE)
    drive_motor.on_for_degrees(SpeedPercent(DRIVE_SPEED), 20)
    for i in range(4):
        control_motor.on_for_degrees(TURN_SPEED, 2 * TURN_ANGLE)
        drive_motor.on_for_degrees(SpeedPercent(DRIVE_SPEED), DEGREE_TURN)
        drive_motor.off()
        time.sleep(0.5)
        control_motor.on_for_degrees(TURN_SPEED, - 2 * TURN_ANGLE)
        drive_motor.on_for_degrees(SpeedPercent(-DRIVE_SPEED), DEGREE_TURN + 5)
        drive_motor.off()
        time.sleep(0.5)
    control_motor.on_for_degrees(TURN_SPEED, TURN_ANGLE)
