#!/usr/bin/env python3
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, UltrasonicSensor

u_distance = UltrasonicSensor(INPUT_1)
ls_r = LightSensor(INPUT_2)  # rechter Sensor auf Input 2
ls_c = LightSensor(INPUT_3)  # center Sensor auf Input 3 # neuer Sensor
ls_l = LightSensor(INPUT_4)  # links Sensor auf Input 4

def init_threshold() -> tuple(int,int):
    light_ping_l = ls_l.reflected_light_intensity
    light_ping_c = ls_c.reflected_light_intensity
    light_ping_r = ls_r.reflected_light_intensity

    white = (light_ping_l + light_ping_r) / 2
    black = light_ping_c

    return (white,black)

def update_threshold(light_ping_l, light_ping_c, light_ping_r, old_values) -> tuple(int,int):

    white = old_values[0]
    black = old_values[1]
    
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
    
    return (white,black)


def fetch_sensor(values: tuple(int,int)):

    threshhold = (values[0] + values[1]) // 2
    
    # ((ls_l, lsr mittelwert für weiß) ls_c für schwarz) mittelwert für threshhold
    light_ping_l = ls_l.reflected_light_intensity
    light_ping_c = ls_c.reflected_light_intensity
    light_ping_r = ls_r.reflected_light_intensity

    update_threshold(light_ping_l,light_ping_c,light_ping_r,values)

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
