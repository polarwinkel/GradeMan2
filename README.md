# GradeMan2

Lehrer- und Notenassistent

## Was ist GradeMan2 / What is this ?

#### [Deutsch]

GradeMan2 ist die komplett neue Version des seit einem Jahrzehnt bewährten Unterrichts- und Notenmanagers GradeMan. Die ultimative Unterrichtsmanagement-Lösung für Lehrer!

Im Gegensatz zum [GradeMan Classic](https://github.com/polarwinkel/GradeMan/), der eher als Ein-Rechner-Lösung gedacht war, ist GradeMan2 auf den Einsatz als persönliche Cloud-Lösung optimiert, mit responsive design, dark-mode, integrierter Schülerbild-Kamera etc.. Aber auch als PC-Lösung ist GradeMan2 ebenfalls einsetzbar.

#### [English]

GradeMan2 is the all-new version of the GradeMan school management system for teachers.

As long as nobody else translates this it will only be available in german language. Please contact me if you want to make a translation!

## Stable Release

GradeMan2 ist mit der Version 2.0.0 bereit für den breiten Einsatz!

Ich habe GradeMan2 schon das ganze Schuljahr 2020/21 in Prokuktiveinsatz, alle Features laufen einwandfrei. Nur noch wenige Komfortfunktionen stehen noch auf meiner ToDo-Liste (s.u.), die per Update dann noch bei Zeiten kommen.

Meine ToDo-Liste:

- Bereitstellung einer Windows-exe-Datei oder eines Windows-Installers
- ~~berechnete Notenvorschläge für die Halbjahre~~
- Sitzplaneditor (bislang: Sitzpläne müssen manuell als CSV erstellt werden, siehe Doku in GradeMan2)

## Wie kann ich GradeMan2 verwenden?

### Linux

Die einfachste Möglichkeit ist es die `.deb`-Paketdatei für z.B. Debian, Ubuntu und ähnliche Debian-Derivate herunterzuladen und zu installieren. (In dieser ist GradeMan2 als Quelltext-Version enthalten und kann zur Überprüfung der Vertrauenswürdigkeit auch vollständig eingesehen werden.)

Nach der Installation des Paketes findet sich ein eintrag im Startmenü unter "Lernprogramme" welches den Server startet, der sich als Tray-Icon bemerkbar macht. Die Benutzeroberfläche lässt sich per Rechtsklick darauf und dann einem Klick auf `Start` mit dem Browser öffnen.

GradeMan2 ist dann im Browser unter `http://localhost:4202` erreichbar, die Daten werden standardmäßig in der `grademan.sqlite3`-Datei in Heimverzeichnis gespeichert (kann in GradeMan2 angepasst werden).

### Windows

Bislang: Die verwendete Programmiersprache Python3 muss manuell installiert werden, siehe dazu [die Webseite von python](https://www.python.org/downloads/windows/).

Die Abhängigkeiten von Python3-Bibliotheken müssen dann durch einmaliges Ausführen der folgenden Befehlszeile (Eingabeaufforderung) installiert werden:

```
pip install flask waitress markdown jinja2 pyyaml wxWidgets
```

GradeMan2 kann dann als `.zip`-Datei heruntergeladen werden und durch Doppelklick auf `GradeMan2Tray.py` gestartet werden.

TODO: Eine .exe-Datei oder ein Installer ist noch in Planung (vgl. Inhalt des Ordners `buildExe`), als nicht-Windows-Nutzer nehme ich hier gerne Hilfe an!

### GradeMan2-Server

#### [Deutsch]

Die beste Möglichkeit GradeMan2 zu nutzen ist ein eigener GradeMan2-Server, z.B. auf einem Raspberry Pi zu Hause.

Ich empfehle dann den Zugriff z.B. über einen nginx-Reverse-Proxy abzusichern mit Zugangsdaten und ssl-Verschlüsselung (z.B. let's Encrypt). Alternativ geht es vermutlich auch, wenn man z.B. in seinem Heimrouter einen VPN-Zugang einrichtet, was aber weniger Komfortabel ist.

Das ist aber auch der komplizierteste Weg, der Erfahrung mit Servern erfordert! Unbezahlte Hilfe kann ich hierfür leider nicht leisten.

Wer mit den folgenden Stichworten klarkommt wird es aber sicher schnell schaffen:

- DynDNS für den Zugang nach Hause (bei dynamischer IP-Adresse)
- Zertifikate, z.B. von let's Encrypt, für die Transport-Verschlüsselung (zwingend nötig damit die Fotografie-Funktion für Schülerfotos funktioniert)
- Reverse-Proxy, z.B. `nginx` für das Routing "nach draußen"
- Port-Forwarding im Heimrouter

Meine funktionierende Konfiguration für `nginx`:

```
server {
        listen 443 ssl default_server;
        listen [::]:443 ssl default_server;
        server_name your.tld www.your.tld; # replace your.tld
        ssl_certificate /etc/letsencrypt/live/your.tld/fullchain.pem; # replace your.tld
        ssl_certificate_key /etc/letsencrypt/live/your.tld/privkey.pem; # replace your.tld
        # GradeMan
        location / { # optional something like: `/GradeMan2/` (GradeMan2 always uses relative paths)
                proxy_pass              http://192.168.x.y/; # replace x and y! ; The `/` is important!
                proxy_set_header        Host            $host;
                proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header        X-Remote-User $remote_user;
                auth_basic              "Auth required!";
                auth_basic_user_file    GradeMan2.passwd;
        }
}
```

#### [English]

The best way to use GradeMan2 is to set up your personal GradeMan2-Server, i.e. on a Raspberry Pi. Then Access GradeMan2 from any of your devices, like your Desktop, Smartphone, Tablet, a School-PC or whatever over the web.

I recommend to use a reverse proxy like nginx for access control and ssl-encryption.

But: You will need quite some experience in IT-Administration on Linux to make it happen!
