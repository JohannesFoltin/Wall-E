#!/usr/bin/env python3
import time
from math import tanh
from ev3dev2.sensor import INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, ColorSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B
from ev3dev2.motor import LargeMotor, SpeedPercent

drive_motor = LargeMotor(OUTPUT_B)
control_motor = LargeMotor(OUTPUT_A)
steer_ls_r = LightSensor(INPUT_3)
steer_ls_l = ColorSensor(INPUT_4)
currentAngle = 0

def follow_line():
    tm1 = 2  # turning Multiplikator
    drive_motor.on(SpeedPercent(-20))
    while True:
        ref1 = steer_ls_r.reflected_light_intensity
        ref2 = steer_ls_l.reflected_light_intensity # neuer Sensor
        print(ref2)
        if ref2 > 16 and currentAngle != 30:
            print("SCHWARZ")
            control_motor.on_for_degrees(SpeedPercent(100), 30)
            currentAngle = 30
        if ref2 < 16 and currentAngle == 30 :
            control_motor.on_for_degrees(SpeedPercent(100), -30)
            currentAngle = 0
        time.sleep(1)
