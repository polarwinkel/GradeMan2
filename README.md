# GradeMan2

Lehrer- und Notenassistent

## Was ist GradeMan2 / What is this ?

#### [Deutsch]

GradeMan2 ist die komplett neue Version des seit einem Jahrzehnt bewährten Unterrichts- und Notenmanagers GradeMan. Die ultimative Unterrichtsmanagement-Lösung für Lehrer!

#### [English]

GradeMan2 is the all-new version of the GradeMan schoon management system for teachers.

As long as nobody else translates this it will only be available in german language. Please contact me if you want to make a translation!

## Public Release Candidate

GradeMan2 ist zum Sommer 2021 bereit für den breiten Einsatz!

Ich habe GradeMan2 schon das ganze Schuljahr 2020/21 in Prokuktiveinsatz, alle Features laufen einwandfrei. Nur noch wenige Komfortfunktionen stehen noch auf meiner ToDo-Liste, die per Update dann noch kommen.

Das Einzige, was noch nicht fertig ist, ist das Packaging als Debian-Paket und Windows-exe. Ich versuche das noch bis zum Schuljahresbeginn 2021/22 fertig zu bekommen.

## Wie kann ich GradeMan2 starten?

### Linux

Bislang: GradeMan2 herunterladen, dafür sorgen dass python3, python3-jinja2 und python3-wxgtk4.0 installiert sind, und dann die GradeMan2Tray.py ausführen.

Der GradeMan2-Server ist dann als Taskbar-Icon zu sehen, die Benutzeroberfläche lässt sich per Rechtsklick darauf und dann einem Klick auf `Start` mit dem Browser öffnen.

TODO: Ein .deb-Paket ist noch in Arbeit!

### Windows

Bislang: Siehe oben, wie unter Linux!

TODO: Eine .exe-Datei ist noch in Arbeit!

### GradeMan2-Server

#### [Deutsch]

Die beste Möglichkeit GradeMan2 zu nutzen ist ein eigener GradeMan2-Server, z.B. auf einem Raspberry Pi zu Hause.

Ich empfehle dann den Zugriff z.B. über einen nginx-Reverse-Proxy abzusichern mit Zugangsdaten und ssl-Verschlüsselung. Alternativ geht es vermutlich auch, wenn man z.B. in seinem Heimrouter einen VPN-Zugang einrichtet, was aber weniger Komfortabel ist.

Das ist aber auch der komplizierteste Weg, der einiges an Erfahgung in der Linux-IT-Administration erfordert!

#### [English]

The best way to use GradeMan2 is to set up your personal GradeMan2-Server, i.e. on a Raspberry Pi. Then Access GradeMan2 from any of your devices, like your Desktop, Smartphone, Tablet, a School-PC or whatever over the web.

I recommend to use a reverse proxy like nginx for access control and ssl-encryption.

But: You will need quite some experience in IT-Administration on Linux to make it happen. Maybe I'll make this easier some day or create a HowTo for this.
