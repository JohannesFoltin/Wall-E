#!/usr/bin/env python3
from time import sleep
from ev3dev2.motor import OUTPUT_A
from ev3dev2.motor import LargeMotor, SpeedPercent

lm = LargeMotor(OUTPUT_A)
lm.on_for_rotations(SpeedPercent(100),5)
