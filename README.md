# Schlemmen Ohne Grenzen

Die Webseite für Schlemmen Ohne Grenzen. Realisiert mit Django und Bootstrap.

## Setup

Alle benötigten Abhängigkeiten sind der Datei ```requirements.txt``` enthalten. Um sein System nicht vollzumüllen macht es Sinn, die Entwicklung in einer virtuellen Umgebung durchzuführen. Dazu kann virtualenvwrapper verwendet werden.

Nachdem man virtualenvwrapper installiert hat kann man mit ```mkvirtualenv schlemmen``` ein neues virtualenv erstellen.
Abhängigkeiten (Django, geopy usw.) können nun mit ```pip install -r requirements.txt``` im virtualenv installiert werden.

In Zukunft kann mit dem Befehl ```workon schlemmen``` wieder ins virtualenv gewechselt werden.

Für die Hilfe Seite, die zu bestimmten Zeiten Tipps darstellen kann, wird eine hilfen.py benötigt, die separat deployed werden muss (damit sie keiner der Schlemmer vor dem Event hier finden kann.)

## Start der Development-Umgebung

Mit ```python manage.py runserver``` kann ein Development-Server gestartet werden.

Davor kann es notwendig sein, Datenbankmigrationen durchzuführen. Dies kann man mit ```python manage.py migrate``` machen.
