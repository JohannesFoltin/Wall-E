#!/usr/bin/env python3
import time
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, OUTPUT_C
from ev3dev2.motor import MoveTank, SpeedPercent, MediumMotor

drive_tank = MoveTank(OUTPUT_A, OUTPUT_D)
ball_motor = MediumMotor(OUTPUT_C)

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
TURN_DEGREE = 10  # Inkrement für Korrekturen


# Passt die Ausrichtung des Roboters an, wenn die Linie nicht gefunden wurde.
def turn_angle_white(LastColorState):
    if (LastColorState == LEFT_LS) or (LastColorState == EDGE_L_LS):
        # Fahr mit halber Geschwindigkeit, 4 mal nach rechts
        drive_tank.on_for_degrees(SpeedPercent(HALF_DRIVE_SPEED), SpeedPercent(-HALF_DRIVE_SPEED), 4 * TURN_DEGREE)
    elif (LastColorState == RIGHT_LS) or (LastColorState == EDGE_R_LS):
        # Fahr mit halber Geschwindigkeit, 4 mal nach links
        drive_tank.on_for_degrees(SpeedPercent(-HALF_DRIVE_SPEED), SpeedPercent(HALF_DRIVE_SPEED), 4 * TURN_DEGREE)


# Fahre rückwärts, wenn die Linie nicht gefunden wurde.
def drive_back(currentStateColor, last_state):
    if currentStateColor == NO_LINE_LS:
        if last_state == NO_LINE_LS:
            # Kontinuierlich rückwärts fahren
            drive_tank.on(SpeedPercent(-CONTINUE_SPEED), SpeedPercent(-CONTINUE_SPEED))
        else:
            # 1 mal rückwärts fahren mit voller Geschwindigkeit
            drive_tank.on_for_degrees(SpeedPercent(-DRIVE_SPEED), SpeedPercent(-DRIVE_SPEED), TURN_DEGREE)
        return STATE_NO_LINE, NO_LINE_LS
    else:
        return STATE_FOLLOW_LINE, NO_LINE_LS


# Stoppt den Antrieb des Roboters.
def tank_stop():
    drive_tank.off()
    time.sleep(0.2)


def move_tank_value(direction, Colorstate):
    if Colorstate == NORMAL_LS:
        return True
    if direction > 0:
        drive_tank.on_for_degrees(SpeedPercent(DRIVE_SPEED), SpeedPercent(DRIVE_SPEED), TURN_DEGREE)
    else:
        drive_tank.on_for_degrees(SpeedPercent(DRIVE_SPEED), SpeedPercent(DRIVE_SPEED), -TURN_DEGREE)
    return False


# Führt eine 180° Drehung des Roboters durch.
def turn_tank(turn):
    TURN_WS = 30  # Drehgeschwindigkeit
    # Drehe den Roboter um 180 Grad
    drive_tank.on_for_degrees(SpeedPercent(-TURN_WS), SpeedPercent(TURN_WS), turn)


def deploy_ball():
    ball_motor.on_for_degrees(SpeedPercent(5), -90)  # - geht nach vorne
    time.sleep(1)
    ball_motor.on_for_degrees(SpeedPercent(-5), -90)
    ball_motor.off


# Passt die Bewegung des Roboters basierend auf den Sensordaten / State der Linie an.
def adjust_tank(currentStateColor, last_state, speed):
    save_current_state = NORMAL_LS
    if currentStateColor == NORMAL_LS:
        if last_state == NORMAL_LS:
            # Kontinuierlich geradeaus mit normaler Geschwindigkeit
            if not (speed == 1000):
                drive_tank.on(SpeedPercent(speed), SpeedPercent(speed))
                print("Langsam speed")
            else:
                drive_tank.on(SpeedPercent(CONTINUE_SPEED), SpeedPercent(CONTINUE_SPEED))
        else:
            # 1 mal geradeaus fahren mit voller Geschwindigkeit
            drive_tank.on_for_degrees(SpeedPercent(DRIVE_SPEED), SpeedPercent(DRIVE_SPEED), TURN_DEGREE)
        save_current_state = NORMAL_LS
        print('normal')

    elif currentStateColor == LEFT_LS:
        print('left')
        # leichte Korrektur nach links
        drive_tank.on_for_degrees(SpeedPercent(-HALF_DRIVE_SPEED), SpeedPercent(DRIVE_SPEED), TURN_DEGREE)
        save_current_state = LEFT_LS

    elif currentStateColor == RIGHT_LS:
        print('right')
        # leichte Korrektur nach rechts
        drive_tank.on_for_degrees(SpeedPercent(DRIVE_SPEED), SpeedPercent(-HALF_DRIVE_SPEED), TURN_DEGREE)
        save_current_state = RIGHT_LS

    elif currentStateColor == EDGE_L_LS:
        print('hard left')
        # harte Korrektur nach links
        drive_tank.on_for_degrees(SpeedPercent(-DRIVE_SPEED), SpeedPercent(DRIVE_SPEED), 1.5 * TURN_DEGREE)
        save_current_state = EDGE_L_LS

    elif currentStateColor == EDGE_R_LS:
        print('hard right')
        # harte Korrektur nach rechts
        drive_tank.on_for_degrees(SpeedPercent(DRIVE_SPEED), SpeedPercent(-DRIVE_SPEED), 1.5 * TURN_DEGREE)
        save_current_state = EDGE_R_LS

    elif currentStateColor == NO_LINE_LS:
        # Kontinuierlich geradeaus mit normaler Geschwindigkeit
        if not (speed == 1000):
            drive_tank.on(SpeedPercent(speed), SpeedPercent(speed))
            print("Langsam speed")
        else:
            drive_tank.on(SpeedPercent(CONTINUE_SPEED), SpeedPercent(CONTINUE_SPEED))
        print('no line')
        return STATE_NO_LINE, NO_LINE_LS

    elif currentStateColor == ALL_BLACK:
        if last_state == LEFT_LS or last_state == EDGE_L_LS:
            # harte Korrektur nach links
            drive_tank.on_for_degrees(SpeedPercent(-DRIVE_SPEED), SpeedPercent(DRIVE_SPEED), 1.5 * TURN_DEGREE)
        elif last_state == RIGHT_LS or last_state == EDGE_R_LS:
            # harte Korrektur nach rechts
            drive_tank.on_for_degrees(SpeedPercent(DRIVE_SPEED), SpeedPercent(-DRIVE_SPEED), 1.5 * TURN_DEGREE)
        else:
            # geradeaus fahren für eine kurze Strecke
            drive_tank.on_for_degrees(SpeedPercent(DRIVE_SPEED), SpeedPercent(DRIVE_SPEED), TURN_DEGREE)
        save_current_state = ALL_BLACK
        print('all black')
    return STATE_FOLLOW_LINE, save_current_state
