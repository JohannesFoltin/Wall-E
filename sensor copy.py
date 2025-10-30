#!/usr/bin/env python3
from time import sleep
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import LightSensor

ls_1 = LightSensor(INPUT_1)
ls_2 = LightSensor(INPUT_4)


while True:
    print("is_1: ", ls_1.reflected_light_intensity)
    print("is_1: ", ls_1.ambient_light_intensity)
    print("is_2: ", ls_2.reflected_light_intensity)
    print("is_2: ", ls_2.ambient_light_intensity)
    sleep(3)
