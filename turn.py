#!/usr/bin/env python3
import time
from FetchSensor import fetch_sensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B
from ev3dev2.motor import LargeMotor, SpeedPercent

control_motor = LargeMotor(OUTPUT_A)
drive_motor = LargeMotor(OUTPUT_B)


def turn(values_threshold):
    # if linie weg oder abstand 20cm
    DRIVE_SPEED = 100
    TURN_SPEED = SpeedPercent(80)
    TURN_ANGLE_BACK = 300  # max turn angle
    TURN_ANGLE_FORWARD = 400
    DEGREE_TURN = 500

    control_motor.on_for_degrees(TURN_SPEED, TURN_ANGLE_BACK)
    drive_motor.on_for_degrees(SpeedPercent(DRIVE_SPEED), DEGREE_TURN)
    drive_motor.off()
    time.sleep(0.5)
    control_motor.on_for_degrees(TURN_SPEED, -(TURN_ANGLE_BACK + TURN_ANGLE_FORWARD))
    drive_motor.reset()
    while drive_motor.position < DEGREE_TURN and True not in fetch_sensor(values_threshold):
        drive_motor.on(SpeedPercent(-DRIVE_SPEED))
        time.sleep(0.3)
    drive_motor.off()
    control_motor.on_for_degrees(TURN_SPEED, TURN_ANGLE_FORWARD)
