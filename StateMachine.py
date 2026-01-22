#!/usr/bin/env python3
from AdjustTank import adjust_tank, turn_angle_white, drive_back, tank_stop, turn_tank, move_tank_value
from FetchSensor import fetch_sensor, init_threshold, update_threshold, fetch_distance


STATE_FOLLOW_LINE = 0
STATE_TURN_ARROUND = 1
STATE_WALL = 2
STATE_HAS_BALL = 3
STATE_PUSH_BLOCK = 4
STATE_TROW_BALL = 5
STATE_NO_LINE = 6
current_state = STATE_FOLLOW_LINE
LastColorState = None
prev_time = 0

HAS_TURNED = False
HAS_PUSHED = False
HAS_BALL = 0  # 0: nicht gemacht, 1: steht vor Schranke, 2: gemacht


# Globale State Machine
def State_machine():
    # Init der nötigen Werte
    global current_state, HAS_TURNED, HAS_BALL, HAS_PUSHED, prev_time
    # Threshold einlesen
    values_threshold = init_threshold()
    # Erster State
    LastColorState = current_state
    distance = 300

    while True:
        distance, prev_time = fetch_distance(prev_time, distance)
        values_threshold = update_threshold(values_threshold)
        # Schranken händling

        if distance <= 100 and HAS_BALL != 2:
            current_state = STATE_WALL

        if current_state == STATE_FOLLOW_LINE:
            # Threshold updaten
            # Fahre und kriege den neuen state
            current_state, LastColorState = adjust_tank(fetch_sensor(values_threshold), LastColorState, 1000)

        elif current_state == STATE_NO_LINE:
            if not HAS_TURNED:
                # 180° Drehung am Anfang des Parcours
                turn_tank()
                HAS_TURNED = True
            else:
                previous_state = current_state  # Speichert, wie die Linie verlassen wurde
                # Fahre weiter und suche die Linie, wenn nicht gefunden, zurückfahren und erneut suchen
                for i in range(9):
                    value = move_tank_value(1,fetch_sensor(values_threshold)) # 1 Cm nach vorne
                    if value:
                        #BARCODE i länge
                        print("ASd")
                    
                for _ in range(12):

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
        elif current_state == STATE_WALL:
            # Schranke
            if (HAS_BALL == 1) and (distance > 22):
                HAS_BALL = 2
                current_state = STATE_FOLLOW_LINE
            elif (distance <= 19) and (not (HAS_BALL == 2)) and HAS_TURNED:
                tank_stop()
                HAS_BALL = 1
                print("gar nicht fahren")
            elif HAS_BALL == 0:
                current_state, LastColorState = adjust_tank(fetch_sensor(values_threshold), LastColorState, -10)
                print("langsamer fahren")
                current_state = STATE_FOLLOW_LINE

        # elif current_state == STATE_PUSH_BLOCK:
        #     push_block()
        #     # TODO drive_back to line
        #     current_state = STATE_FOLLOW_LINE
        # elif current_state == STATE_TROW_BALL:
        #     pass


State_machine()
