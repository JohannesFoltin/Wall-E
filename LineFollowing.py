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

currentAngle = 0  # Links: -200 Rechts: +200
max_turn_angle = 400
newSensorBlacks = 15  # s (alles drunter ist schwarz) für smaller wie jannes dick
oldSensorBlacks = 35


def fetch_sensor():
    light_ping_l = ls_l.reflected_light_intensity
    light_ping_c = ls_c.reflected_light_intensity
    light_ping_r = ls_r.reflected_light_intensity

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

    return (black_l, black_c, black_r)


def follow_line():
    global currentAngle, max_turn_angle

    NORMAL_LS = (False, True, False)  # LS = LIGHT STATE
    LEFT_LS = (True, True, False)
    RIGHT_LS = (False, True, True)
    EDGE_L_LS = (True, False, False)
    EDGE_R_LS = (False, False, True)
    NO_LINE_LS = (False, False, False)

    RIGHT_WS = -400  # WHEEL TURN STATE
    LEFT_WS = 400
    STRAIGHT_WS = 0

    correction_time = 2
    drive_speed = -10

    drive_motor.on(SpeedPercent(drive_speed))
    while True:
        currentStateColor = fetch_sensor()
        print(currentStateColor)

        if currentAngle == RIGHT_WS:
            print("RightWS")
            if currentStateColor == RIGHT_LS:
                continue
            elif currentStateColor == NORMAL_LS:
                control_motor.on_for_degrees(SpeedPercent(100), LEFT_WS)
                currentAngle = STRAIGHT_WS
            elif currentStateColor == LEFT_LS:
                control_motor.on_for_degrees(SpeedPercent(100), 2 * LEFT_WS)
                currentAngle = LEFT_WS
            # new code, das gleiche für edge_L_LS
            elif currentStateColor == EDGE_R_LS:
                print('Edge_Rechts')
                # TODO weiter nach links, schleife: wenn dann NO_LINE_LS: correction
                while currentStateColor == EDGE_R_LS:
                    currentStateColor = fetch_sensor()
                if currentStateColor == NO_LINE_LS:
                    # TODO correction nach hinten links
                    print('Korregiere links zurueck')
                    drive_motor.off
                    time.sleep(0.3)
                    control_motor.on_for_degrees(SpeedPercent(100), 1.5 * LEFT_WS)

                    drive_motor.on_for_seconds(SpeedPercent(-drive_speed), correction_time)
                    drive_motor.off
                    time.sleep(0.3)
                    control_motor.on_for_degrees(SpeedPercent(100), 0.5 * RIGHT_WS)
                    currentAngle = STRAIGHT_WS
                    drive_motor.on(SpeedPercent(drive_speed))
        elif currentAngle == LEFT_WS:
            print("LeftWs")
            if currentStateColor == RIGHT_LS:
                control_motor.on_for_degrees(SpeedPercent(100), 2 * RIGHT_WS)
                # TODO
                currentAngle = RIGHT_WS
            elif currentStateColor == NORMAL_LS:
                control_motor.on_for_degrees(SpeedPercent(100), RIGHT_WS)
                currentAngle = STRAIGHT_WS
            elif currentStateColor == LEFT_LS:
                continue
            elif currentStateColor == EDGE_L_LS:
                print('Edge_Links')
                # TODO weiter nach links, schleife: wenn dann NO_LINE_LS: correction
                while currentStateColor == EDGE_L_LS:
                    currentStateColor = fetch_sensor()
                if currentStateColor == NO_LINE_LS:
                    # TODO correction nach hinten links
                    print('Korregiere rechts zurueck')
                    drive_motor.off
                    time.sleep(0.3)
                    control_motor.on_for_degrees(SpeedPercent(100), 1.5 * RIGHT_WS)

                    drive_motor.on_for_seconds(SpeedPercent(-drive_speed), correction_time)
                    drive_motor.off
                    time.sleep(0.3)
                    control_motor.on_for_degrees(SpeedPercent(100), 0.5 * LEFT_WS)
                    currentAngle = STRAIGHT_WS
                    drive_motor.on(SpeedPercent(drive_speed))
        elif currentAngle == STRAIGHT_WS:
            print("StraightWs")
            if ((currentStateColor == RIGHT_LS)
                    or (currentStateColor == EDGE_R_LS)):
                control_motor.on_for_degrees(SpeedPercent(100), RIGHT_WS)
                # TODO
                currentAngle = RIGHT_WS
            elif currentStateColor == NORMAL_LS:
                continue
            elif ((currentStateColor == LEFT_LS)
                  or (currentStateColor == EDGE_L_LS)):
                control_motor.on_for_degrees(SpeedPercent(100), LEFT_WS)
                # TODO
                currentAngle = LEFT_WS

        time.sleep(0.01)


follow_line()
