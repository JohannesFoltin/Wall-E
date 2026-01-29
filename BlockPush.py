#!/usr/bin/env python3
import time
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveTank, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, UltrasonicSensor
from FetchSensor import fetch_sensor, init_threshold, update_threshold, fetch_distance

ls_r = LightSensor(INPUT_1)  # rechter Sensor auf Input 1
ls_c = LightSensor(INPUT_2)  # center Sensor auf Input 2
ls_l = LightSensor(INPUT_3)  # links Sensor auf Input 3
uss_distance = UltrasonicSensor(INPUT_4)  # Abstandssensor auf Input 4


drive_tank = MoveTank(OUTPUT_A, OUTPUT_D)

STATE_FOLLOW_LINE = 0
STATE_TURN_ARROUND = 1
STATE_GATE = 2
STATE_PUSH_BLOCK = 3
STATE_TROW_BALL = 4
STATE_NO_LINE = 5

NORMAL_LS = (False, True, False)  # LS = LIGHT STATE
LEFT_LS = (True, True, False)
RIGHT_LS = (False, True, True)
EDGE_L_LS = (True, False, False)
EDGE_R_LS = (False, False, True)
ALL_BLACK = (True, True, True)
NO_LINE_LS = (False, False, False)

DRIVE_SPEED = -50  # Fahrgeschwindigkeit zum Korrigieren
CONTINUE_SPEED = DRIVE_SPEED * 0.6  # Kontinuierliche Fahrgeschwindigkeit
HALF_DRIVE_SPEED = 0.5 * DRIVE_SPEED  # Fahrgeschwindigkeit für leichte Korrekturen
NO_LINE_SPEED = DRIVE_SPEED * 0.8
TURN_DEGREE = 10  # Inkrement für Korrekturen

MARK_DEGREE = -100


def push_block():
    # TODO push block
    # fahr rückwärts um senkrecht zur linie zu stehen
    drive_tank.on_for_degrees(SpeedPercent(DRIVE_SPEED), SpeedPercent(DRIVE_SPEED), 20)
    # dreh 90 grad
    TURN_WS = 30  # Drehgeschwindigkeit
    # Drehe den Roboter um 90 Grad
    drive_tank.on_for_degrees(SpeedPercent(-TURN_WS), SpeedPercent(TURN_WS), 210)
    prev_time = 0
    on_block = False
    while True:
        distance, prev_time = fetch_distance(prev_time, distance)
        values_threshold = update_threshold(values_threshold)
        if distance < 5:
            on_block = True
            current_state, LastColorState = adjust_tank(fetch_sensor(values_threshold), LastColorState, -10)
        if (distance > 8 and on_block) or distance > 100:
            break
        else:
            current_state, LastColorState = adjust_tank(fetch_sensor(values_threshold), LastColorState, 1000)

    drive_tank.on_for_degrees(SpeedPercent(DRIVE_SPEED), SpeedPercent(DRIVE_SPEED), 20)
    # dreh 90 grad
    TURN_WS = 30  # Drehgeschwindigkeit
    # Drehe den Roboter um 90 Grad
    drive_tank.on_for_degrees(SpeedPercent(-TURN_WS), SpeedPercent(TURN_WS), 420)

    while True:
        distance, prev_time = fetch_distance(prev_time, distance)
        values_threshold = update_threshold(values_threshold)
        current_state, LastColorState = adjust_tank(fetch_sensor(values_threshold), LastColorState, 1000)
        if LastColorState == ALL_BLACK:
            drive_tank.on_for_degrees(SpeedPercent(-DRIVE_SPEED), SpeedPercent(0.5 * DRIVE_SPEED), 210)
            return
        
