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
barcode_count = 0

HAS_TURNED = False
HAS_PUSHED = False
HAS_BALL = 0  # 0: nicht gemacht, 1: steht vor Schranke, 2: gemacht
HAS_BLOCK = 0 # 0: nicht geschoben, 1: zum block gedreht, 2: sthet vor block 3: block geschoben


# Globale State Machine
def State_machine():
    # Init der nötigen Werte
    global current_state, HAS_TURNED, HAS_BALL, HAS_BLOCK, HAS_PUSHED, prev_time, barcode_count
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
            print("Wir fangen an mit der Schranke")
            current_state = STATE_WALL

        # find barcode
        if barcode_count >= 3:
            print("Wir fangen an mit dem Block pushen")
            current_state = STATE_PUSH_BLOCK

        if current_state == STATE_FOLLOW_LINE:
            # Fahre und kriege den neuen state
            current_state, LastColorState = adjust_tank(fetch_sensor(values_threshold), LastColorState, 1000)

        elif current_state == STATE_NO_LINE:
            print("No Line")
            if not HAS_TURNED:
                # 180° Drehung am Anfang des Parcours
                turn_tank(420)
                HAS_TURNED = True
            else:
                previous_color_state = LastColorState  # Speichert, wie die Linie verlassen wurde
                # Fahre weiter und suche die Linie, wenn nicht gefunden, zurückfahren und erneut suchen
                for i in range(18):  # max lochgröße
                    print(f"Lochgröße: {i}")
                    value = move_tank_value(1, fetch_sensor(values_threshold))  # 0.5 Cm nach vorne
                    if value:
                        if i < 4:  # Barcodegröße
                            print(f"Lochgröße final: {i}")
                            barcode_count += 1
                            current_state = STATE_FOLLOW_LINE
                            break
                tank_stop()
                print("Fahr rueckwaerts")
                turn_angle_white(previous_color_state)  # vlt nach drive_back
                for _ in range(20):
                    current_state, LastColorState = drive_back(fetch_sensor(values_threshold), LastColorState)
                    print("go_back")
                    if current_state != STATE_NO_LINE:
                        tank_stop()
                        current_state = STATE_FOLLOW_LINE
                        break
        elif current_state == STATE_WALL:
            # Schranke
            print("Schranke")
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

        elif current_state == STATE_PUSH_BLOCK:
            while True:
                print('Fick Johannes!')
                break

            if HAS_BLOCK == 0:  # noch nicht geschoben
                # 20 cm vorwärts
                for i in range(18):
                    values_threshold = update_threshold(values_threshold)
                    _, LastColorState = adjust_tank(fetch_sensor(values_threshold), LastColorState, 1000)
                # 90° drehung
                turn_tank(105)
                HAS_BLOCK = 1
            elif HAS_BLOCK == 1:  # zur linie gedreht
                if distance <= 5:
                    HAS_BLOCK = 2
                current_state, LastColorState = adjust_tank(fetch_sensor(values_threshold), LastColorState, 1000)
            elif HAS_BLOCK == 2:  # steht vor Block
                current_state, LastColorState = adjust_tank(fetch_sensor(values_threshold), LastColorState, -10)
                if distance > 5:  # wie weit fliegt der block weg
                    HAS_BLOCK = 3
            elif HAS_BLOCK == 3:  # block geschoben
                for i in range(6):  # 3cm rückwärts
                    _ = move_tank_value(-1, fetch_sensor(values_threshold))  # 0.5 Cm nach vorne
                turn_tank(420)


            BlockPush()
            # TODO drive_back to line
            current_state = STATE_FOLLOW_LINE
        # elif current_state == STATE_TROW_BALL:
        #     pass


State_machine()
