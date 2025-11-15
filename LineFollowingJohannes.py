#!/usr/bin/env python3
import time
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, ColorSensor, UltrasonicSensor, Sensor
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

def follow_line():
    global currentAngle, max_turn_angle

    black_l = False  # 0-Schwarz, 1-Grau, 2-Weiß
    black_c = True
    black_r = False
    # Schwarz = True

    NORMAL_LS = (False, True, False)  # LS = LIGHT STATE
    LEFT_LS = (True, True, False)
    RIGHT_LS = (False, True, True)
    EDGE_L_LS = (True, False, False)
    EDGE_R_LS = (False, False, True)
    NO_LINE_LS = (False, False, False)

    RIGHT_WS = -400  # WHEEL TURN STATE
    LEFT_WS = 400
    STRAIGHT_WS = 0

    correction_time = 1.5
    drive_speed = 10

    drive_motor.on(SpeedPercent(drive_speed))
    while True:
        light_ping_l = ls_l.reflected_light_intensity
        light_ping_c = ls_c.reflected_light_intensity + 23
        light_ping_r = ls_r.reflected_light_intensity

        print("Lights: ")
        print(light_ping_l)
        print(light_ping_c)
        print(light_ping_r)
        print("\n")

        averageValue = (light_ping_c + light_ping_l + light_ping_r)/3

        difference_light_l = (light_ping_l - averageValue)/averageValue
        difference_light_c = (light_ping_c - averageValue)/averageValue
        difference_light_r = (light_ping_r - averageValue)/averageValue


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

        currentStateColor = (black_l, black_c, black_r)
        print("Cuurrren")
        print(currentStateColor)
        if currentAngle == RIGHT_WS:
            print("RightWS")
            if currentStateColor == RIGHT_LS:
                print("Do nothing")
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
                while True:
                    # currentStateColor = fetch_sensor() # funktion zur sensor auslese und verarbeitung
                    if currentStateColor == NO_LINE_LS:
                        # TODO correction nach hinten links
                        print('Korregiere links zurück')
                        drive_motor.off
                        control_motor.on_for_degrees(SpeedPercent(100), 2 * LEFT_WS)
                        drive_motor.on_for_seconds(SpeedPercent(-drive_speed), correction_time)
                        drive_motor.off
                        control_motor.on_for_degrees(SpeedPercent(100), RIGHT_WS)
                        drive_motor.on(SpeedPercent(drive_speed))
                        break
                    elif ((currentStateColor == NORMAL_LS)
                          or (currentStateColor == RIGHT_LS)
                          or (currentStateColor == LEFT_LS)
                          or (currentStateColor == EDGE_L_LS)):
                        # linie wieder gefunden
                        print("linie wieder gefunden")
                        break
        elif currentAngle == LEFT_WS:
            print("LeftWs")
            if currentStateColor == RIGHT_LS:
                print("Reifen auf -200 drehen")
                control_motor.on_for_degrees(SpeedPercent(100), 2 * RIGHT_WS)
                # TODO
                currentAngle = RIGHT_WS
            elif currentStateColor == NORMAL_LS:
                print("Reifen wieder auf 0 drehen")
                control_motor.on_for_degrees(SpeedPercent(100), RIGHT_WS)
                currentAngle = STRAIGHT_WS
            elif currentStateColor == LEFT_LS:
                print("Do nothing")
                continue
        elif currentAngle == STRAIGHT_WS:
            print("StraightWs")
            if currentStateColor == RIGHT_LS:
                control_motor.on_for_degrees(SpeedPercent(100), RIGHT_WS)
                # TODO
                currentAngle = RIGHT_WS
            elif currentStateColor == NORMAL_LS:
                print("Do nothging")
                continue
            elif currentStateColor == LEFT_LS:
                control_motor.on_for_degrees(SpeedPercent(100), LEFT_WS)
                # TODO
                currentAngle = LEFT_WS

        time.sleep(0.2)


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
                pass

                if ((black_l, black_c, black_r) == (True, False, True)) and (currentAngle != 0):  # white, black, white
            if currentAngle is True:  # if tires are turned: turn back to unturned
                #control_motor.on_for_degrees(SpeedPercent(100), -currentAngle)
                currentAngle = turn_angle
                print("turn back")
        elif ((black_l, black_c, black_r) == (False, False, True)) and (currentAngle == 0):  # black, black, white
            # turn left
            #control_motor.on_for_degrees(SpeedPercent(100), turn_angle)
            currentAngle = -turn_angle
            print("turn left")
        elif (black_l, black_c, black_r) == (True, False, False):  # white, black, black
            # turn right
            #control_motor.on_for_degrees(SpeedPercent(100), -turn_angle)
            currentAngle = turn_angle
            print("turn right")
        elif (black_l, black_c, black_r) == (False, True, True):  # black, white, white
            # backwards left
            drive_motor.off()
            #control_motor.on_for_degrees(SpeedPercent(100), -backwards_turn_angle)
            #drive_motor.on_for_seconds(SpeedPercent(100), backwards_turn_time)
            #drive_motor.on(SpeedPercent(50))
            print("backwards left")
        elif (black_l, black_c, black_r) == (True, True, False):  # white, white, black
            # backwards right
            drive_motor.off()
            #control_motor.on_for_degrees(SpeedPercent(100), backwards_turn_angle)
            #drive_motor.on_for_seconds(SpeedPercent(100), backwards_turn_time)
            #drive_motor.on(SpeedPercent(50))
            print("backwards right")
        elif (black_l, black_c, black_r) == (True, True, True):  # white, white, white
            # check white time to distinguish stage mark | hole | line lost
            pass'''
