#!/usr/bin/env python3
import time
import math
from time import sleep
from ev3dev2.sensor import INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, ColorSensor, UltrasonicSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B
from ev3dev2.motor import LargeMotor, SpeedPercent


class WallE(object):

    def __init__(self):

        self.THERSHOLD = 30
        self.STATE_SAFE_ON_TABLE = 1
        self.STATE_EDGE_DETECTED = 2

        self.drive_motor = LargeMotor(OUTPUT_B)
        self.control_motor = LargeMotor(OUTPUT_A)
        self.steer_ls_r = LightSensor(INPUT_3)
        self.steer_ls_l = ColorSensor(INPUT_4)
        self.u_distance = UltrasonicSensor(INPUT_2)
        self.state = self.STATE_SAFE_ON_TABLE

    def drive(self):
        self.mt.on(SpeedPercent(50),SpeedPercent(50))
        if self.ls.reflected_light_intensity <= self.THERSHOLD:
            self.state = self.STATE_EDGE_DETECTED
        else:
<<<<<<< HEAD
            self.state = self.STATE_SAFE_ON_TABLE
=======
            self.state = self.STATE_SAFE_ON_TABLE
>>>>>>> 37c2c61e41efeb1dcf991b55984eea1738ffd0fa

    def turn_around(self):
        pass

    def main(self):
        while True:
            if self.state == self.STATE_SAFE_ON_TABLE:
                self.drive()
            if self.state == self.STATE_EDGE_DETECTED:
                self.turn_around()
            sleep(0.01)


if __name__ == '__main__':
    sm = WallE()
    sm.main()
