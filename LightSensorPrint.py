#!/usr/bin/env python3
from time import sleep
from ev3dev2.sensor import INPUT_3, INPUT_4, INPUT_2
from ev3dev2.sensor.lego import ColorSensor, LightSensor
from ev3dev2.motor import OUTPUT_C
from ev3dev2.motor import LargeMotor, SpeedPercent, MediumMotor

#u_distance = UltrasonicSensor(INPUT_1)
ls_r = LightSensor(INPUT_2)  # rechter Sensor auf Input 2
ls_c = LightSensor(INPUT_3)  # center Sensor auf Input 3 # neuer Sensor
ls_l = LightSensor(INPUT_4)  # links Sensor auf Input 4

# ball_motor = MediumMotor(OUTPUT_C)
# ball_motor.on_for_degrees(SpeedPercent(5), -90)
# ball_motor.off

# refer = ls_c.value()

while True:
    ls_c.mode =  ls_c.MODE_RGB_RAW

    print("is_l: ", ls_l.reflected_light_intensity)

    print("is_c: ", ls_c.reflected_light_intensity)
    print("is_r: ", ls_r.reflected_light_intensity)
    #print("is_c ref: ", ls_c.reflected_light_intensity)

    # print("is_r: ", ls_r.reflected_light_intensity)
    # value_c = ls_c.value()
    # if abs(value_c - refer) <= refer * 0.05:
    #     refer = value_c
    # print(refer)
    # print("Errechnte Werte")
    # light_ping_l = ls_l.reflected_light_intensity
    # light_ping_r = ls_r.reflected_light_intensity

    # averageValue = (light_ping_l + light_ping_r)/2

    # difference_light_l = (light_ping_l - averageValue)/averageValue
    # difference_light_r = (light_ping_r - averageValue)/averageValue

    # print(difference_light_l)
    # print(difference_light_r)


    sleep(0.5)
