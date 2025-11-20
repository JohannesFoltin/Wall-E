#!/usr/bin/env python3
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, ColorSensor, UltrasonicSensor

u_distance = UltrasonicSensor(INPUT_1)
ls_r = LightSensor(INPUT_2)  # rechter Sensor auf Input 2
ls_c = ColorSensor(INPUT_3)  # center Sensor auf Input 3 # neuer Sensor
ls_l = LightSensor(INPUT_4)  # links Sensor auf Input 4


def fetch_sensor():
    newSensorBlacks = 15  # s (alles drunter ist schwarz) für smaller wie jannes dick n
    oldSensorBlacks = 35

    # ((ls_l, lsr mittelwert für weiß) ls_c für schwarz) mittelwert für threshhold
    light_ping_l = ls_l.reflected_light_intensity
    light_ping_c = ls_c.reflected_light_intensity
    light_ping_r = ls_r.reflected_light_intensity

    # sensor left
    if light_ping_l <= oldSensorBlacks:  # black
        black_l = True
    elif light_ping_l > oldSensorBlacks:
        black_l = False  # white

    # sensor center
    if light_ping_c <= newSensorBlacks:  # blackk
        black_c = True
    elif light_ping_c > newSensorBlacks:
        black_c = False  # white

    # sensor right
    if light_ping_r <= oldSensorBlacks:  # black
        black_r = True
    elif light_ping_r > oldSensorBlacks:
        black_r = False  # white

    return (black_l, black_c, black_r)
