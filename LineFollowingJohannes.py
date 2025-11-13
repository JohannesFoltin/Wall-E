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
newSensorBlacks = 15  # s (alles drunter ist schwarz) für smaller wie jannes dick
oldSensorBlacks = 35

def follow_line():
    global currentAngle, max_turn_angle
    start_time = time.time()
    backwards_turn_angle = max_turn_angle
    backwards_turn_time = 1
    black_l = False  # 0-Schwarz, 1-Grau, 2-Weiß
    black_c = True
    black_r = False
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
        if light_ping_l <= oldSensorBlacks:  # black
            black_l = True
        elif light_ping_l > oldSensorBlacks:
            black_l = False  # white

        # sensor center
        if light_ping_c <= newSensorBlacks:  # black
            black_c = True
        elif light_ping_c > newSensorBlacks:
            black_c = False  # white

        # sensor right
        if light_ping_r <= oldSensorBlacks:  # black
            black_r = True
        elif light_ping_r > oldSensorBlacks:
            black_r = False  # white
        
        if (black_l, black_c, black_r) == (True, False, True):  # white, black, white
            if currentAngle is True:  # if tires are turned: turn back to unturned
                control_motor.on_for_degrees(SpeedPercent(100), -currentAngle)
                currentAngle = True
        elif (black_l, black_c, black_r) == (False, False, True):  # black, black, white
            # turn left
            control_motor.on_for_degrees(SpeedPercent(100), turn_angle)
            currentAngle = -turn_angle
        elif (black_l, black_c, black_r) == (True, False, False):  # white, black, black
            # turn right
            control_motor.on_for_degrees(SpeedPercent(100), -turn_angle)
            currentAngle = turn_angle
        elif (black_l, black_c, black_r) == (False, True, True):  # black, white, white
            # backwards left
            drive_motor.off()
            control_motor.on_for_degrees(SpeedPercent(100), -backwards_turn_angle)
            drive_motor.on_for_seconds(SpeedPercent(100), backwards_turn_time)
        elif (black_l, black_c, black_r) == (True, True, False):  # white, white, black
            # backwards right
            drive_motor.off()
            control_motor.on_for_degrees(SpeedPercent(100), backwards_turn_angle)
            drive_motor.on_for_seconds(SpeedPercent(100), backwards_turn_time)
            drive_motor.on(SpeedPercent(50))
        elif (black_l, black_c, black_r) == (True, True, True):  # white, white, white
            # check white time to distinguish stage mark | hole | line lost
            pass

        time.sleep(0.2)
        end_time = time.time()
        print("Zeit" + str(end_time - start_time))


follow_line()

'''if black_lost_start_time is None:
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
                pass'''
