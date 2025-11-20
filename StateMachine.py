import time
from LineFollowing import adjust_wheels, fetch_sensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, ColorSensor, UltrasonicSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B
from ev3dev2.motor import LargeMotor, SpeedPercent

control_motor = LargeMotor(OUTPUT_A)
drive_motor = LargeMotor(OUTPUT_B)
STATE_FOLLOW_LINE = 0
current_state = STATE_FOLLOW_LINE


def State_machine():
    global current_state, STATE_FOLLOW_LINE
    while current_state == STATE_FOLLOW_LINE:

        adjust_wheels()
        time.sleep(0.3)


State_machine()



    drive_motor.on(SpeedPercent(drive_speed))
    currentStateColor = fetch_sensor()
    print(currentStateColor)