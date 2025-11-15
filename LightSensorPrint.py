#!/usr/bin/env python3
from time import sleep
from ev3dev2.sensor import INPUT_3, INPUT_4, INPUT_2
from ev3dev2.sensor.lego import Sensor, ColorSensor, LightSensor

#u_distance = UltrasonicSensor(INPUT_1)
ls_r = Sensor(INPUT_2)  # rechter Sensor auf Input 2
ls_c = Sensor(INPUT_3)  # center Sensor auf Input 3 # neuer Sensor
ls_l = Sensor(INPUT_4)  # links Sensor auf Input 4


while True:
    ls_r = Sensor(INPUT_2)  # rechter Sensor auf Input 2
    ls_c = ColorSensor(INPUT_3)  # center Sensor auf Input 3 # neuer Sensor
    ls_l = Sensor(INPUT_4)
    print("is_l: ", ls_l.value())
    print("is_c: ", ls_c.value())
    print("is_r: ", ls_r.value())
    sleep(1)
