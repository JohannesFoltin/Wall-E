#!/usr/bin/env python3
from time import sleep
from ev3dev2.sensor import INPUT_1,INPUT_2
from ev3dev2.sensor.lego import LightSensor, ColorSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B
from ev3dev2.motor import LargeMotor, SpeedPercent

drive_motor = LargeMotor(OUTPUT_A)
control_motor = LargeMotor(OUTPUT_B)
steer_ls_l = LightSensor(INPUT_1)
steer_ls_r = LightSensor(INPUT_2)


def follow_line():
    while True:
        drive_motor.on_for_seconds(10,1)
        ref1 = steer_ls_l.reflected_light_intensity()
        ref2 = steer_ls_r.reflected_light_intensity()
        if ref1 > ref2:
            print("DEINE MUDDA IST FETTT")
            print("is_1: ", ls_1.reflected_light_intensity)
            print("is_1: ", ls_1.ambient_light_intensity)
            print("is_2: ", ls_2.reflected_light_intensity)
            print("is_2: ", ls_2.ambient_light_intensity)
        elif ref1 < ref2:
            print("DEINE MUTTER IST RECHT SPORTLICH")
    sleep(1)
    

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