#!/usr/bin/env python3
from time import sleep
from AdjustTank import adjust_tank, turn_angle_white, tank_stop, turn_tank, move_tank_value, deploy_ball, ALL_BLACK, NO_LINE_LS
from FetchSensor import fetch_sensor, init_threshold, update_threshold, fetch_distance


STATE_FOLLOW_LINE = 0
STATE_TURN_ARROUND = 1
STATE_WALL = 2
STATE_HAS_BALL = 3
STATE_PUSH_BLOCK = 4
STATE_TROW_BALL = 5
STATE_NO_LINE = 6

HAS_TURNED = False
HAS_BALL = 0  # 0: nicht gemacht, 1: steht vor Schranke, 2: gemacht
HAS_BLOCK = 0  # 0: nicht geschoben, 1: zum block gedreht, 2: steht vor block 3: block geschoben und gedreht


# Globale State Machine
def State_machine():
    # Init der nötigen Werte
    global current_state, HAS_TURNED, HAS_BALL, HAS_BLOCK, prev_time, barcode_count
    prev_time = 0
    barcode_count = 0
    # Threshold einlesen
    values_threshold = init_threshold()
    # Erster State
    current_state = STATE_FOLLOW_LINE
    LastColorState = current_state #???
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
        
        print("HAS_BALL:")
        print(HAS_BALL)
        print()
        print("Barcode:")
        print(barcode_count)
        # find barcode
        if barcode_count >= 3 and LastColorState != NO_LINE_LS:
            if HAS_BALL != 2 or HAS_BLOCK == 3:
                barcode_count = 0
            else:
                print("Wir fangen an mit dem Block pushen")
                current_state = STATE_PUSH_BLOCK

        if HAS_BALL == 2 and LastColorState == ALL_BLACK and distance <= 10:  # change 10
            current_state = STATE_TROW_BALL
        
        print("state:")
        print(current_state)

        if current_state == STATE_FOLLOW_LINE:
            # Fahre und kriege den neuen state
            current_state, LastColorState = adjust_tank(fetch_sensor(values_threshold), LastColorState, 1000)

        elif current_state == STATE_NO_LINE:
            print("State_No Line")
            if not HAS_TURNED:
                # 180° Drehung am Anfang des Parcours
                turn_tank(420)
                HAS_TURNED = True
                current_state = STATE_FOLLOW_LINE
            else:
                previous_color_state = LastColorState  # Speichert, wie die Linie verlassen wurde
                # Fahre weiter und suche die Linie, wenn nicht gefunden, zurückfahren und erneut suchen
                tmpende = False
                for i in range(18):  # max lochgröße
                    print("Lochgroesse: ")
                    print(i)
                    value = move_tank_value(1, fetch_sensor(values_threshold))  # 0.5 Cm nach vorne
                    if value:
                        if 1< i < 4:  # Barcodegröße
                            print("Lochgroesse final: ")
                            print(i)
                            barcode_count += 1
                            current_state = STATE_FOLLOW_LINE
                            tmpende = True
                if not tmpende:
                    tank_stop()
                    print("Fahr rueckwaerts")
                    turn_angle_white(previous_color_state)  # vlt nach drive_back
                    for _ in range(24):
                        tmp = move_tank_value(-1, fetch_sensor(values_threshold))
                        print("go_back")
                        if tmp:
                            tank_stop()
                            current_state = STATE_FOLLOW_LINE
                            break
                    current_state = STATE_FOLLOW_LINE
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

        elif current_state == STATE_PUSH_BLOCK:
            if HAS_BLOCK == 0:  # noch nicht geschoben
                # 20 cm vorwärts
                for _ in range(18):
                    values_threshold = update_threshold(values_threshold)
                    current_state, LastColorState = adjust_tank(fetch_sensor(values_threshold), LastColorState, 1000)
                # 90° drehung
                turn_tank(180)
                HAS_BLOCK = 1
            elif HAS_BLOCK == 1:  # zur linie gedreht
                if distance <= 5:
                    HAS_BLOCK = 2
                current_state, LastColorState = adjust_tank(fetch_sensor(values_threshold), LastColorState, 1000)
            elif HAS_BLOCK == 2:  # steht vor Block
                current_state, LastColorState = adjust_tank(fetch_sensor(values_threshold), LastColorState, 1000) # 100
                if distance > 5:  # wie weit fliegt der block weg
                    for _ in range(6):  # 3cm rückwärts
                        _ = move_tank_value(-1, 0)  # 0.5 Cm nach vorne
                    turn_tank(420)
                    HAS_BLOCK = 3
            elif HAS_BLOCK == 3:  # block geschoben und gedreht
                _, LastColorState = adjust_tank(fetch_sensor(values_threshold), LastColorState, 1000)
                if LastColorState == NO_LINE_LS:
                    turn_tank(50)
                    for _ in range(4):
                        value = move_tank_value(1, fetch_sensor(values_threshold))  # 0.5 Cm nach vorne
                        if value:
                            break
                    current_state = STATE_FOLLOW_LINE

        elif current_state == STATE_TROW_BALL:
            _, LastColorState = adjust_tank(fetch_sensor(values_threshold), LastColorState, 1000)
            while distance > 5:
                _,value = adjust_tank(fetch_sensor(values_threshold), LastColorState, 1000)
                distance, prev_time = fetch_distance(prev_time, distance)

            deploy_ball()
            exit()


if __name__ == "__main__":
    State_machine()
