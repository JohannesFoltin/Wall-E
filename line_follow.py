#!/usr/bin/env python3
from time import sleep
from math import tanh
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import LightSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B
from ev3dev2.motor import LargeMotor, SpeedPercent

drive_motor = LargeMotor(OUTPUT_A)
control_motor = LargeMotor(OUTPUT_B)
steer_ls_l = LightSensor(INPUT_1)
steer_ls_r = LightSensor(INPUT_4)


def follow_line():
    tt = 0.75  # turning time
    tm1 = 2  # turning multiplikator 1
    tm2 = 2  # turning multiplikator 2
    error_rate = 0
    drive_motor.on(SpeedPercent(20))
    while True:
        ref1 = steer_ls_l.reflected_light_intensity
        ref2 = steer_ls_r.reflected_light_intensity
        error = ref1 - ref2
        if ref1 > ref2:
            control_motor.on_for_degrees(45 * tanh(tm1 * error + tm2 * error_rate ), tt)  # oder arctan
            control_motor.on_for_degrees(-45 * tanh(tm * error), tt)

            print("DEINE MUDDA IST FETTT")
        elif ref1 < ref2:
            control_motor.on_for_degrees(-45 * tanh(tm * error), tt)
            control_motor.on_for_degrees(45 * tanh(tm * error), tt)
            print("DEINE MUTTER IST RECHT SPORTLICH")
        sleep(0.1)


follow_line()
'''
wall-e.on_for_rotations(SpeedPercent(100),5)

    SpeedDPS(degrees_per_second, desc=None)
    SpeedPercent(percent, desc=None)
    ls = LightSensor(INPUT_1) # oder 'ColorSensor(INPUT_1)'
print(ls.reflected_light_intensity)
print(ls.ambient_light_intensity)
sleep(3)

'''
