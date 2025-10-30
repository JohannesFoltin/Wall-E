#!/usr/bin/env python3
import sys
from time import sleep
from ev3dev2.sensor import INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, ColorSensor

ls_1 = LightSensor(INPUT_3)
ls_2 = ColorSensor(INPUT_4)


while True:
    print("is_1: ", ls_1.reflected_light_intensity)
    print("is_2: ", ls_2.reflected_light_intensity)
    sleep(3)
