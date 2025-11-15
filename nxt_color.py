#pragma config(Sensor, S4,  color, sensorEV3_Color_Infared) // S4 = Port 4

task main()
{
    while (true)
    {
        // Modus „Reflected Light“
        SetSensorMode(color, modeEV3Color_Reflected);
        int reflected = SensorRaw[color];          // ‑1023

        // Modus „Ambient Light“
        SetSensorMode(color, modeEV3Color_Ambient);
        int ambient   = SensorRaw[color];

        // Modus „RGB“
        SetSensorMode(color, modeEV3Color_RGB);
        int r = SensorRaw[color];      // Rot (‑1023)
        int g = SensorRaw[color+1];    // Grün
        int b = SensorRaw[color+2];    // Blau

        // Ausgabe via Display
        Display.clearScreen();
        TextOut(, LCD_LINE1 "Ref:%d", reflected);
        TextOut(, LCD_LINE2, "Amb:%d", ambient);
        TextOut(, LCD_LINE3, "R:%d G:%d B:%d", r,g,b);
        Wait(200);
    }
}
