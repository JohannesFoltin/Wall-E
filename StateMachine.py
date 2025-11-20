import time
from LineFollowing import adjust_wheels
from FetchSensor import fetch_sensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, ColorSensor, UltrasonicSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B
from ev3dev2.motor import LargeMotor, SpeedPercent

control_motor = LargeMotor(OUTPUT_A)
drive_motor = LargeMotor(OUTPUT_B)
STATE_FOLLOW_LINE = 0
current_state = STATE_FOLLOW_LINE
currentAngle = 0


def State_machine():
    global current_state, STATE_FOLLOW_LINE, currentAngle
    drive_motor.on(SpeedPercent(10))
    while current_state == STATE_FOLLOW_LINE:
        currentAngle = adjust_wheels(fetch_sensor, currentAngle)
        time.sleep(0.3)


State_machine()
