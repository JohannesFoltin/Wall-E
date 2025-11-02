#!/usr/bin/env python3
from time import sleep
from ev3dev2.motor import OUTPUT_B, OUTPUT_A
from ev3dev2.motor import LargeMotor, SpeedPercent

drive_motor = LargeMotor(OUTPUT_B)
control_motor = LargeMotor(OUTPUT_A)

control_motor.on_for_degrees(SpeedPercent(100), -60)
while True:
    drive_motor.on(SpeedPercent(-100))
