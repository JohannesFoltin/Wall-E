#!/usr/bin/env python3
from time import sleep
from ev3dev2.sensor import INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, ColorSensor

ls_1 = LightSensor(INPUT_3)
ls_2 = ColorSensor(INPUT_4)


while True:
    print("is_1: ", ls_1.reflected_light_intensity * 100 / 47.900000000000006)
    print("is_2: ", ls_2.reflected_light_intensity * 100 / 17)
    sleep(3)
