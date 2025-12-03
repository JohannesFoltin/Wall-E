#!/usr/bin/env python3

from typing import tuple

from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, UltrasonicSensor

ls_r = LightSensor(INPUT_1)  # rechter Sensor auf Input 1
ls_c = LightSensor(INPUT_2)  # center Sensor auf Input 2
ls_l = LightSensor(INPUT_3)  # links Sensor auf Input 3


def read_ls_raw() -> tuple[float]:
    """Ließt die Rohwerte der Lichtsensoren aus (rechts, mitte, links)"""
    return(ls_r.reflected_light_intensity, ls_c.reflected_light_intensity, ls_l.reflected_light_intensity)

def init_threshold():
    right, center, left = read_ls_raw()
    white = (left + right) / 2
    black = center

    return (white, black)


def update_threshold(old_values):
    white, black = old_values
    readings = read_ls_raw()

    white = max(white, max(readings))
    black = min(black, min(readings))

    return (white, black)

def fetch_sensor(values):
   """Mittelwert aus Wieß und Schwarz, dann die Spannweite zwischen Weiß und Schwarz. 
   Gibt den Mittelwert minus den Rohwert geteilt durch die Spanne aus
   Liefert für jeden Sensor die Abweichung vom aktuellen Wert.

    Gibt aus für:
        > 0  -> Sensor sieht „dunkler“ als der gespeicherte Wert -> linie
        < 0  -> Sensor sieht „heller“ als der gespeicherte Wert -> Hintergrund
        Betrag nahe 0 -> kaum Unterschied

    Die Abweichungen werden in einem Bereich von ca. -1.0 .. +1.0 liegen."""
    white, black = values
    threshold = (white + black) / 2.0
    span = max(1.0, white - black) #damit nicht im return durch 0 geteilt wird

    readings = read_ls_raw()
    """# sensor left
    if light_ping_l <= threshhold:  # black
        black_l = True
    elif light_ping_l > threshhold:
        black_l = False  # white

    # sensor center
    if light_ping_c <= threshhold:  # black
        black_c = True
    elif light_ping_c > threshhold:
        black_c = False  # white

    # sensor right
    if light_ping_r <= threshhold:  # black
        black_r = True
    elif light_ping_r > threshhold:
        black_r = False  # white

    return (black_l, black_c, black_r)"""
    return tuple((threshold - value) / span for value in readings)