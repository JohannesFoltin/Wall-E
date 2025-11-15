#!/usr/bin/env python3
from ev3dev2.sensor import INPUT_3
from ev3dev2.sensor.lego import ColorSensor
import time

# Sensor-Objekt an Port 4
cs = ColorSensor(INPUT_3)

# Zu prüfende Modi
MODES = {
    'REFLECTED': cs.MODE_COL_REFLECT,
    'AMBIENT':   cs.MODE_COL_AMBIENT,
    'COLOR_ID': cs.MODE_COL_COLOR,
    'RGB_RAW':  cs.MODE_RGB_RAW
}

def read_sensor(mode_name):
    cs.mode = MODES[mode_name]
    time.sleep(.05)                     # kurze Stabilisation
    if mode_name == 'RGB_RAW':
        r, g, b = cs.raw   # tuple (‑1023)
        return {'R': r, 'G': g, 'B': b}
    else:
        return cs.value()               # int ‑1023 bzw. Farb‑ID

# Beispielschleife
while True:
    reflected = read_sensor('REFLECTED')
    ambient   = read_sensor('AMBIENT')
    color_id  = read_sensor('COLOR_ID')
    rgb       = read_sensor('RGB_RAW')
    #print(f"Reflected={reflected:4d}  Ambient={ambient:4d}  "
    #      f"ColorID={color_id:2d}  RGB={rgb}")
    print(reflected)
    print(ambient)
    print(color_id)
    print(rgb)
    time.sleep(.5)
