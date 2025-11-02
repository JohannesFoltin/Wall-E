#!/usr/bin/env python3
import time
from ev3dev2.sensor import INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, ColorSensor, UltrasonicSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B
from ev3dev2.motor import LargeMotor, SpeedPercent

drive_motor = LargeMotor(OUTPUT_B)
control_motor = LargeMotor(OUTPUT_A)
steer_ls_r = LightSensor(INPUT_3)
steer_ls_l = ColorSensor(INPUT_4)
u_distance = UltrasonicSensor(INPUT_2)


def turn():
    # if linie weg | abstand 20cm
    turn_time = 2.0
    turn_angle = -60.0
    min_distance = 5
    while True:
        drive_motor.off()
        turn_angle *= -1
        control_motor.on_for_degrees(SpeedPercent(100), turn_angle)
        drive_motor.on(100)
        start = time.time()
        while True:
            if start - time.time() > turn_time:
                break
            elif u_distance.distance_centimeters_ping < min_distance:
                break


turn()
