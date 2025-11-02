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


def follow_line():
    tm1 = 2  # turning multiplikator 1
    drive_motor.on(SpeedPercent(-20))
    while True:
        ref1 = steer_ls_r.reflected_light_intensity * 100 / 47.900000000000006
        ref2 = steer_ls_l.reflected_light_intensity * 100 / 17
        error = ref1 - ref2
        error_threshold = 5  # ka
        turn_rad = 60 * tanh(tm1 * error)
        if error > error_threshold:
            if ref1 > ref2:
                control_motor.on_for_degrees(SpeedPercent(100), turn_rad)
                control_motor.on_for_degrees(SpeedPercent(100), -turn_rad)
                print("DEINE MUDDA IST FETTT")
            elif ref1 < ref2:
                control_motor.on_for_degrees(SpeedPercent(100), -turn_rad)
                control_motor.on_for_degrees(SpeedPercent(100), turn_rad)
                print("DEINE MUTTER IST RECHT SPORTLICH")


follow_line()
'''
wall-e.on_for_rotations(SpeedPercent(100),5)

SpeedDPS(degrees_per_second, desc=None)
SpeedPercent(percent, desc=None)
ls = LightSensor(INPUT_1) # oder 'ColorSensor(INPUT_1)'
print(ls.reflected_light_intensity)
print(ls.ambient_light_intensity)
sleep(3)

start = time.time()
end = time.time()
verstrichene_zeit = end - start
'''
