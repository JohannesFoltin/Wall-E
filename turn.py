#!/usr/bin/env python3
import time
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, ColorSensor, UltrasonicSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B
from ev3dev2.motor import LargeMotor, SpeedPercent

control_motor = LargeMotor(OUTPUT_A)
drive_motor = LargeMotor(OUTPUT_B)

u_distance = UltrasonicSensor(INPUT_1)
ls_r = LightSensor(INPUT_2)  # rechter Sensor auf Input 2
ls_c = ColorSensor(INPUT_3)  # center Sensor auf Input 3 # neuer Sensor
ls_l = LightSensor(INPUT_4)  # links Sensor auf Input 4


def turn():
    # if linie weg oder abstand 20cm
    drive_speed = 100
    turn_angle_back = 300  # max turn angle
    turn_angle_for = 400
    degree_turn = 500
    control_motor.on_for_degrees(SpeedPercent(80), turn_angle_back)
    drive_motor.on_for_degrees(SpeedPercent(drive_speed), degree_turn)
    drive_motor.off()
    time.sleep(0.5)
    control_motor.on_for_degrees(SpeedPercent(80), -(turn_angle_back + turn_angle_for))
    drive_motor.on_for_degrees(SpeedPercent(drive_speed), -degree_turn)
    drive_motor.off()
