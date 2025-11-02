#!/usr/bin/env python3
import time
from math import tanh
from ev3dev2.sensor import INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, ColorSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B
from ev3dev2.motor import LargeMotor, SpeedPercent

drive_motor = LargeMotor(OUTPUT_B)
control_motor = LargeMotor(OUTPUT_A)

ls_r = LightSensor(INPUT_2)  # rechter Sensor auf Input 2
ls_c = LightSensor(INPUT_3)  # center Sensor auf Input 3
ls_l = ColorSensor(INPUT_4)  # links Sensor auf Input 4
currentAngle = 0


def follow_line():
    global currentAngle
    tm1 = 2  # turning Multiplikator
    drive_motor.on(SpeedPercent(-20))
    while True:
        ref1 = ls_r.reflected_light_intensity
        ref2 = ls_l.reflected_light_intensity  # neuer Sensor
        ref3 = ls_c.reflected_light_intensity
        print(ref2)
        if ref2 < 3 and currentAngle != 30:
            print("SCHWARZ")
            control_motor.on_for_degrees(SpeedPercent(100), -60)
            currentAngle = 30
        if ref2 > 6 and currentAngle == 30:
            print("zurck")
            control_motor.on_for_degrees(SpeedPercent(100), 60)
            currentAngle = 0
        time.sleep(0.2)


follow_line()
