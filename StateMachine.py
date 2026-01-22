#!/usr/bin/env python3
from AdjustTank import adjust_tank, turn_angle_white, drive_back, tank_stop, turn_tank
from FetchSensor import fetch_sensor, init_threshold, update_threshold, fetch_distance


STATE_FOLLOW_LINE = 0
STATE_TURN_ARROUND = 1
STATE_GATE = 2
STATE_PUSH_BLOCK = 3
STATE_TROW_BALL = 4
STATE_NO_LINE = 5
current_state = STATE_FOLLOW_LINE
LastColorState = None
tims = 0

HAS_TURNED = False
HAS_PUSHED = False
HAS_BALL = 0


# Globale State Machine
def State_machine():
    # Init der nötigen Werte
    global current_state, HAS_TURNED, HAS_BALL, HAS_PUSHED, tims
    # Threshold einlesen
    values_threshold = init_threshold()
    # Erster State
    LastColorState = current_state
    distance = 300

    while True:
        if current_state == STATE_FOLLOW_LINE:
            distance, tims = fetch_distance(tims, distance)
            values_threshold = update_threshold(values_threshold)
            if distance <= 100:
                if (HAS_BALL == 1) and (distance > 22):
                    HAS_BALL = 2
                    continue
                if (distance <= 19) and (not (HAS_BALL == 2)) and HAS_TURNED:
                    tank_stop()
                    current_state, LastColorState = adjust_tank(fetch_sensor(values_threshold), LastColorState, 0)
                    HAS_BALL = 1
                    print("gar nicht fahren")
                    continue
                elif HAS_BALL == 0:
                    current_state, LastColorState = adjust_tank(fetch_sensor(values_threshold), LastColorState, -10)
                    print("langsamer fahren")
                    continue
            # Threshold updaten
            # Fahre und kriege den neuen state
            current_state, LastColorState = adjust_tank(fetch_sensor(values_threshold), LastColorState, 1000)

        elif current_state == STATE_NO_LINE:
            values_threshold = update_threshold(values_threshold)
            if not HAS_TURNED:
                # 180° Drehung am Anfang des Parcours
                turn_tank()
                HAS_TURNED = True
            else:
                previous_state = current_state  # Speichert, wie die Linie verlassen wurde
                # Fahre weiter und suche die Linie, wenn nicht gefunden, zurückfahren und erneut suchen
                for _ in range(12):
                    if distance <= 100 and HAS_BALL == 0:
                        current_state, LastColorState = adjust_tank(fetch_sensor(values_threshold), LastColorState, -10)
                    else:
                        current_state, LastColorState = adjust_tank(fetch_sensor(values_threshold), LastColorState, 1000)
                    print("lost")
                    if current_state != STATE_NO_LINE:
                        current_state = STATE_FOLLOW_LINE
                        print("found")
                        break
                else:
                    tank_stop()
                    turn_angle_white(previous_state)
                    for _ in range(16):
                        current_state, LastColorState = drive_back(fetch_sensor(values_threshold), LastColorState)
                        print("go_back")
                        if current_state != STATE_NO_LINE:
                            tank_stop()
                            current_state = STATE_FOLLOW_LINE
                            break

        # elif current_state == STATE_PUSH_BLOCK:
        #     push_block()
        #     # TODO drive_back to line
        #     current_state = STATE_FOLLOW_LINE
        # elif current_state == STATE_TROW_BALL:
        #     pass


State_machine()
