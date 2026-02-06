#!/usr/bin/env python3
from AdjustTank import adjust_tank, turn_angle_white, tank_stop, turn_tank, move_tank_value, deploy_ball, ALL_BLACK, NO_LINE_LS,NORMAL_LS
from FetchSensor import fetch_sensor, init_threshold, update_threshold, fetch_distance


STATE_FOLLOW_LINE = 0
STATE_TURN_ARROUND = 1
STATE_WALL = 2
STATE_HAS_BALL = 3
STATE_TROW_BALL = 5
STATE_NO_LINE = 6

HAS_TURNED = True
HAS_BALL = 2  # 0: nicht gemacht, 1: steht vor Schranke, 2: gemacht


# Globale State Machine
def State_machine():
    # Init der nötigen Werte
    global current_state, HAS_TURNED, HAS_BALL, prev_time, barcode_count
    prev_time = 0
    barcode_count = 0
    # Threshold einlesen
    values_threshold = init_threshold()
    # Erster State
    current_state = STATE_FOLLOW_LINE
    LastColorState = NORMAL_LS
    distance = 300

    while True:
        distance, prev_time = fetch_distance(prev_time, distance)

        print("Distance:")
        print(distance)
        print()

        values_threshold = update_threshold(values_threshold)

        # Schranken händling
        if distance <= 50 and HAS_BALL != 2 and HAS_TURNED and LastColorState != NO_LINE_LS:
            print("Wir fangen an mit der Schranke")
            current_state = STATE_WALL

        if HAS_BALL == 2 and LastColorState == ALL_BLACK and distance <= 20:  # change 10
            current_state = STATE_TROW_BALL

        print("state:")
        print(current_state)

        if current_state == STATE_FOLLOW_LINE:
            # Fahre und kriege den neuen state
            current_state, LastColorState = adjust_tank(fetch_sensor(values_threshold), LastColorState, 1000)

        elif current_state == STATE_NO_LINE:
            values_threshold = update_threshold(values_threshold)
            if not HAS_TURNED:
                # 180° Drehung am Anfang des Parcours
                turn_tank(420)
                HAS_TURNED = True
            else:
                barcode_count += 1
                prevColorState = LastColorState  # Speichert, wie die Linie verlassen wurde
                # Fahre weiter und suche die Linie, wenn nicht gefunden, zurückfahren und erneut suchen
                for _ in range(16):
                    value = move_tank_value(1, fetch_sensor(values_threshold))
                    print("lost")
                    if value:
                        current_state = STATE_FOLLOW_LINE
                        print("found")
                        break
                else:
                    tank_stop()
                    turn_angle_white(prevColorState)
                    for _ in range(20):
                        value = move_tank_value(-1, fetch_sensor(values_threshold))
                        print("go_back")
                        if value:
                            tank_stop()
                            current_state = STATE_FOLLOW_LINE
                            print("found")
                            break

        elif current_state == STATE_WALL:
            # Schranke
            print("Schranke")
            if (HAS_BALL == 1) and (distance > 32):
                HAS_BALL = 2
                current_state = STATE_FOLLOW_LINE
            elif (distance <= 19) and (not (HAS_BALL == 2)):
                tank_stop()
                HAS_BALL = 1
                print("gar nicht fahren")
            elif HAS_BALL == 0:
                current_state, LastColorState = adjust_tank(fetch_sensor(values_threshold), LastColorState, -10)
                print("langsamer fahren")
                current_state = STATE_FOLLOW_LINE

        elif current_state == STATE_TROW_BALL:
            _, LastColorState = adjust_tank(fetch_sensor(values_threshold), LastColorState, 1000)
            while distance > 5:
                _, value = adjust_tank(fetch_sensor(values_threshold), LastColorState, 1000)
                distance, prev_time = fetch_distance(prev_time, distance)
            deploy_ball()
            exit()


if __name__ == "__main__":
    State_machine()
