import time
from ev3dev2.motor import OUTPUT_A, OUTPUT_D
from ev3dev2.motor import MoveTank, SpeedPercent

drive_tank = MoveTank(OUTPUT_A, OUTPUT_D)

DRIVE_SPEED = -50  # Fahrgeschwindigkeit zum Korrigieren
TURN_DEGREE = 10  # Inkrement für Korrekturen

i = 0
while True:
    drive_tank.on_for_degrees(SpeedPercent(DRIVE_SPEED), SpeedPercent(DRIVE_SPEED), TURN_DEGREE)
    i += 1
    print(i)
    time.sleep(0.5)
