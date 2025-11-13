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
currentAngle = 0
max_turn_angle = 400
newSensorBlacks = 15 # s (alles drunter ist schwarz) für smaller wie jannes dick
oldSensorBlacks = 35

def follow_line():
    global currentAngle, max_turn_angle
    start_time = time.time()
    backwards_turn_angle = max_turn_angle
    backwards_turn_time = 1
    color_l = 0  # 0-Schwarz, 1-Grau, 2-Weiß
    color_c = 0
    color_r = 0
    #drive_motor.on(SpeedPercent(-20))
    while True:
        light_ping_l = ls_l.reflected_light_intensity
        light_ping_c = ls_c.reflected_light_intensity
        light_ping_r = ls_r.reflected_light_intensity
        print(light_ping_l)
        print(light_ping_c)
        print(light_ping_r)
        turn_angle = max_turn_angle

        # sensor left
        if light_ping_l < 3:  # black
            color_l = 0
        elif light_ping_l > 6:
            color_l = 2  # white
        else:
            color_l = 1  # gray

        # sensor center
        if light_ping_c < 3:  # black
            color_c = 0
        elif light_ping_c > 6:
            color_c = 2  # white
        else:
            color_c = 1  # gray

        # sensor right
        if light_ping_r < 3:  # black
            color_r = 0
        elif light_ping_r > 6:
            color_r = 2  # white
        else:
            color_r = 1  # gray

        if (color_l, color_c, color_r) == (0, 2, 0):  # white, black, white
            if currentAngle != 0:  # if tires are turned: turn back to unturned
                control_motor.on_for_degrees(SpeedPercent(100), -currentAngle)
                currentAngle = 0
        elif (color_l, color_c, color_r) == (2, 2, 0):  # black, black, white
            # turn left
            control_motor.on_for_degrees(SpeedPercent(100), turn_angle)
            currentAngle = -turn_angle
        elif (color_l, color_c, color_r) == (0, 2, 2):  # white, black, black
            # turn right
            control_motor.on_for_degrees(SpeedPercent(100), -turn_angle)
            currentAngle = turn_angle
        elif (color_l, color_c, color_r) == (2, 0, 0):  # black, white, white
            # backwards left
            drive_motor.off()
            control_motor.on_for_degrees(SpeedPercent(100), -backwards_turn_angle)
            drive_motor.on_for_seconds(SpeedPercent(100), backwards_turn_time)
        elif (color_l, color_c, color_r) == (0, 0, 2):  # white, white, black
            # backwards right
            drive_motor.off()
            control_motor.on_for_degrees(SpeedPercent(100), backwards_turn_angle)
            drive_motor.on_for_seconds(SpeedPercent(100), -backwards_turn_time)
            drive_motor.on(SpeedPercent(50))
        elif (color_l, color_c, color_r) == (0, 0, 0):  # white, white, white
            # check white time to distinguish stage mark | hole | line lost
            if black_lost_start_time is None:
                black_lost_start_time = time.time()
            black_lost_progess_time = time.time() - black_lost_start_time
            if black_lost_progess_time >= 3:
                # line lost
                # Add logic here, e.g., stop motors or search for line
                pass
            elif 2 < black_lost_progess_time < 3:
                # hole
                continue  # Skip to next loop iteration
            elif black_lost_progess_time <= 2:
                # mark
                # Add logic here, e.g., special action for mark
                pass

        time.sleep(0.2)
        end_time = time.time()
        print("Zeit" + str(end_time - start_time))


follow_line()

'''
        if light_ping_l < 3 and currentAngle == 0:
            # if l_sensor right < 3 -> schwarz, and tire isnt turned turn right
            print("SCHWARZ")
            control_motor.on_for_degrees(SpeedPercent(100), -max_turn_angle)
            currentAngle = max_turn_angle
        if light_ping_l > 6 and currentAngle != max_turn_angle:
            # if l_sensor > 6 -> white and tire is turned turn back
            print("zurck")
            control_motor.on_for_degrees(SpeedPercent(100), max_turn_angle)
            currentAngle = 0

        if light_ping_r < 3 and currentAngle == 0:
            # if l_sensor left < 3 and tire isnt turned -> schwarz, turn left
            print("SCHWARZ")
            control_motor.on_for_degrees(SpeedPercent(100), max_turn_angle)
            currentAngle = max_turn_angle
        if light_ping_r > 6 and currentAngle != max_turn_angle:
            # if l_sensor > 6 -> white and tire is turned turn back
            print("zurck")
            control_motor.on_for_degrees(SpeedPercent(100), -max_turn_angle)
            currentAngle = 0'''
