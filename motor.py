#!/usr/bin/env python3
from time import sleep
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, ColorSensor, UltrasonicSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B
from ev3dev2.motor import LargeMotor, SpeedPercent

drive_motor = LargeMotor(OUTPUT_B)
control_motor = LargeMotor(OUTPUT_A)


control_motor.on_for_degrees(SpeedPercent(100), +400)
control_motor.on_for_degrees(SpeedPercent(100), -400)
sleep(1)
control_motor.on_for_degrees(SpeedPercent(100), +400)
sleep(1)
control_motor.on_for_degrees(SpeedPercent(100), +400)

'''# drive_motor.on_for_degrees(SpeedPercent(10), -800)
while True:
    drive_motor.on(SpeedPercent(-100))
    print(drive_motor.degrees)'''
