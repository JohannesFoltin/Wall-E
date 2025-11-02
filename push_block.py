from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import LightSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B
from ev3dev2.motor import LargeMotor, SpeedPercent

drive_motor = LargeMotor(OUTPUT_A)
control_motor = LargeMotor(OUTPUT_B)
steer_ls_l = LightSensor(INPUT_1)
steer_ls_r = LightSensor(INPUT_4)


def push_block():
    # 3 weiße linien
    pass
