#!/usr/bin/env python3
from time import sleep
from ev3dev2.sensor import INPUT_3, INPUT_4, INPUT_2
from ev3dev2.sensor.lego import LightSensor, ColorSensor

#u_distance = UltrasonicSensor(INPUT_1)
ls_r = LightSensor(INPUT_2)  # rechter Sensor auf Input 2
ls_c = ColorSensor(INPUT_3)  # center Sensor auf Input 3 # neuer Sensor
ls_l = LightSensor(INPUT_4)  # links Sensor auf Input 4


while True:
    print("is_l: ", ls_l.reflected_light_intensity)
    print("is_c: ", ls_c.reflected_light_intensity)
    print("is_r: ", ls_r.reflected_light_intensity)
    sleep(1)
