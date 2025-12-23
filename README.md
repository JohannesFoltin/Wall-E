Dies ist das geniale Projekt der genialen Gruppe Kampfroboter/Wall-E in SDP

# Aufgaben für Donnerstag:

- [] Engerer Radius
- [] Dritter Sensor
- [] Reihnfolge schwarz Erkennung implementieren 

# Aufgaben für Zwischenprüfung:

- [ ] Linie folgen
- [x] Wenden
- [ ] Klotz wegschieben
- [ ] Durch nen Tunnel fahren
- [ ] Wechseln der Lichtverhältnisse
- [ ] Bälle halter (mhhhhm)
- [ ] Steigung und Gefälle

# Ideen

- [ ] turn Tank in adjust Tank
- [ ] update threshhold in fetch sensor funktion 

Postiv ist nach rechts
!! positiv zurück !!

# Testen
- ohne sleep
- jede iteration weiter fahren
- no line,
- 90° kurve
- licht beobachten -> range ausgeben
- 

init 35.6 18.400000000000002
end 43.900000000000006 11.0

threshold
init 27
min 27
max 29

# Zwischenbreicht Arbeitsteilung
- Konstruktion und Softwarekonzept
    - [Michi] Grundlegende Kostruktion, als Basis der genaueren, folgenden Beschreibugen 
    - [Johannes] Linienverfolgung, enge Kurven, Streckenunterbrechungen und wechselnde Lichtbedingungen
    - [Kai] Wendevorgang
    - [Michi] Schranke und Ballaufnahme
    - [Jannes] Schwerpunkt und Steigung/Gefälle
    - [Kai -- Michi] Barcode und Klotz verschieben
    - [Jannes] Ballabgabe und Verhalten im Ziel
    - [Johannes | Kai] Allgemeines Softwarekonzept, Regelung / PID
- [Johannes] Fortschritt
- [Jannes | Kai] Fehleranalyse
- [Alle -- Jannes] Weiteres Vorgehen
- [Johannes] Besonderheiten (Wackeln, Linenverlust)
- [Michi] Arbeitsteilung

Sonstige
- [Jannes] Fotos
- Für Flowcharts: https://app.diagrams.net