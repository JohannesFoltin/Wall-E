#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import LightSensor, ColorSensor


class StateMachine(object):

    def __init__(self):    

        self.THERSHOLD = 30
        self.STATE_SAFE_ON_TABLE = 1
        self.STATE_EDGE_DETECTED = 2

        self.ls = LightSensor(INPUT_1) # oder 'ColorSensor(INPUT_1)'
        self.mt = MoveTank(OUTPUT_A, OUTPUT_B)
        self.state = self.STATE_SAFE_ON_TABLE

    def drive(self):
        self.mt.on(SpeedPercent(50),SpeedPercent(50))
        if self.ls.reflected_light_intensity <= self.THERSHOLD:
            self.state = self.STATE_EDGE_DETECTED
        else:
            self.state = self.STATE_SAFE_ON_TABLE
    
    def turn_around(self):
        self.mt.off()
        self.mt.on_for_seconds(SpeedPercent(0), SpeedPercent(-100), 0.8)
        self.state = self.STATE_SAFE_ON_TABLE

    def main(self):
        while True:
            if self.state == self.STATE_SAFE_ON_TABLE:
                self.drive()
            if self.state == self.STATE_EDGE_DETECTED:
                self.turn_around()
            sleep(0.01)

if __name__ == '__main__':
    sm = StateMachine()
    sm.main()
