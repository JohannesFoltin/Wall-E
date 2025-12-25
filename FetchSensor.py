#!/usr/bin/env python3
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, UltrasonicSensor

ls_r = LightSensor(INPUT_1)  # rechter Sensor auf Input 2
ls_c = LightSensor(INPUT_2)  # center Sensor auf Input 3 # neuer Sensor
ls_l = LightSensor(INPUT_3)  # links Sensor auf Input 4
uss_distance = UltrasonicSensor(INPUT_4)


# Lese die Daten der Licht-Sensoren aus und gebe sie als Tuple zurück
def light_ping():
    return ls_l.reflected_light_intensity, ls_c.reflected_light_intensity, ls_r.reflected_light_intensity


# Initialisieren des Thresholds. Zuweisen von Schwarz und Weiß Threshold
def init_threshold():
    light_ping_l, light_ping_c, light_ping_r = light_ping()

    # Der höchste der der drei Sensoren ist der Hellste -> Weiß
    white = max(light_ping_l, light_ping_r, light_ping_c)
    # Der nidrigste der der drei Sensoren ist der Dunkelste -> Schwarz
    black = min(light_ping_l, light_ping_r, light_ping_c)

    return (white, black)


# Der Threshold wird geupdated. Dabei werden die Werte überschrieben,
# wenn der neue eingelesene Wert größer oder kleiner ist als der derzeitige
# Threshold. Bei weiß wird auf einen größeren Wert geachtet, bei Schwarz kleiner.
def update_threshold(old_values):
    light_ping_l, light_ping_c, light_ping_r = light_ping()

    old_white = old_values[0]
    old_black = old_values[1]

    white = max(old_white, light_ping_l, light_ping_c, light_ping_r)
    black = min(old_black, light_ping_l, light_ping_c, light_ping_r)

    # Vergleichen der Werte
    if light_ping_l > white:
        white = light_ping_l
    elif light_ping_l < black:
        black = light_ping_l
    if light_ping_c > white:
        white = light_ping_c
    elif light_ping_c < black:
        black = light_ping_c
    if light_ping_r > white:
        white = light_ping_r
    elif light_ping_r < black:
        black = light_ping_r

    # Gebe die neuen Thresholds zurück
    return (white, black)


# Verrechne die eingehenden Sensoren Daten mit den festgelegten Thresholds.
# Gebe eine tuple an Wahrheitswerten zurück, je nach dem ob ein Sensor auf Schwarz oder Weiß steht
# (Nach unseren Thresholds)
def fetch_sensor(values):
    light_ping_l, light_ping_c, light_ping_r = light_ping()

    threshhold = (values[0] + values[1]) // 2

    # sensor left
    if light_ping_l <= threshhold:  # black
        black_l = True
    elif light_ping_l > threshhold:
        black_l = False  # white

    # sensor center
    if light_ping_c <= threshhold:  # black
        black_c = True
    elif light_ping_c > threshhold:
        black_c = False  # white

    # sensor right
    if light_ping_r <= threshhold:  # black
        black_r = True
    elif light_ping_r > threshhold:
        black_r = False  # white

    return (black_l, black_c, black_r)


# Hole die Daten vom Ultraschall Sensor
def fetch_distance():
    return uss_distance.distance_centimeters
