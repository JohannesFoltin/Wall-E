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
    # if linie weg oder abstand 20cm
    drive_speed = 100
    turn_time = 2  # how long the turned wheels should stay turned
    turn_angle = 400  # max turn angle
    min_distance_wall = 5  # distance to wall, where the turn should stop
    turn_count = 0
    while True:
        turn_angle *= -1  # switch turn direction
        drive_speed *= -1  # switch drive direction to drive backwards
        control_motor.on_for_degrees(SpeedPercent(100), turn_angle)
        drive_motor.on(SpeedPercent(drive_speed))
        start = time.time()
        while time.time() - start < turn_time:
            time.sleep(0.01)
            if u_distance.distance_centimeters_ping < min_distance_wall:
                break
        control_motor.on_for_degrees(SpeedPercent(100), -turn_angle)
        drive_motor.off()
        if turn_count == 4:
            break
        turn_count += 1


turn()
