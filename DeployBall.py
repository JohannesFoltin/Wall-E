ball_motor = MediumMotor(OUTPUT_C)
ball_motor.on_for_degrees(SpeedPercent(5), -90)  # - geht nach vorne
ball_motor.off
