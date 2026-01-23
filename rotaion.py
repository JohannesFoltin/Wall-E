import time
from ev3dev2.motor import OUTPUT_A, OUTPUT_D
from ev3dev2.motor import MoveTank, SpeedPercent

drive_tank = MoveTank(OUTPUT_A, OUTPUT_D)

i = 0
while True:
    drive_tank.on(SpeedPercent(-50), SpeedPercent(-50))
    i += 1
    print(i)
    time.sleep(0.5)
