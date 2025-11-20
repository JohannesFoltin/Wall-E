import time
from LineFollowing import follow_line, fetch_sensor
STATE_FOLLOW_LINE = 0
current_state = STATE_FOLLOW_LINE


def State_machine():
    global current_state, STATE_FOLLOW_LINE
    while current_state == STATE_FOLLOW_LINE:

        follow_line()
        time.sleep(0.3)


State_machine()



    drive_motor.on(SpeedPercent(drive_speed))
    currentStateColor = fetch_sensor()
    print(currentStateColor)