from datetime import datetime

hilfen = [{
    'title': 'Vorspeise 1',
    'datetime': datetime(2017, 6, 21, 18, 0),
    'color': '#cb4154',
    'puzzles': [
        {"id": "r1t1", "title": "Tipp 1", "text": "Fällt euch etwas bei den Namen auf? Sie haben alle etwas gemeinsam."},
        {"id": "r1t2", "title": "Tipp 2", "text": "Alle stehen eindeutig für jeweils eine Straßenbahnlinie in Karlsruhe"},
        {"id": "r1t3", "title": "Tipp 3", "text": "Was haben die Straßenbahnlinien gemeinsam?"},
        {"id": "r1t4", "title": "Tipp 4", "text": "Sie haben einen gemeinsamen Schnittpunkt..."},
        {"id": "r1t5", "title": "Lösung", "text": "Mathystraße"}
        ]
    },
    {
    'title': 'Vorspeise 2',
    'datetime': datetime(2017, 6, 21, 18, 0),
    'color': '#a4c639',
    'puzzles': [
        {"id": "r2t1", "title": "Tipp 1", "text": "Schaut mal auf die Telefontastatur von eurem Handy"},
        {"id": "r2t2", "title": "Tipp 2", "text": "Die Zeichen stehen jeweils für eine Zahl"},
        {"id": "r2t3", "title": "Tipp 3", "text": "Die Telefonnummer ist +49 721 6095 8755. Rufe mal an. (wenn besetzt noch einmal versuchen)"},
        {"id": "r2t4", "title": "Tipp 4", "text": "Das Geräusch steht für einen ganz bekannten Ort in Karlsruhe. Welchen denn?"},
        {"id": "r2t5", "title": "Lösung", "text": "Schlosspark"}
        ]
    },
    {
    'title': 'Vorspeise 3',
    'datetime': datetime(2017, 6, 21, 18, 0),
    'color': '#9966cc',
    'puzzles': [
        {"id": "r3t1", "title": "Tipp 1", "text": "0 bezeichnet den Beginn"},
        {"id": "r3t2", "title": "Tipp 2", "text": "Die Liste von Zahlen und + und - zeigt euch eine Bewegung an"},
        {"id": "r3t3", "title": "Tipp 3", "text": "Ihr beginnt bei Null und geht jeweils zu der Zahl, die euch durch die Angaben in der Liste vorgegeben werden. + 2 3 bedeutet zum Biepisel, dass ihr zu der Zahl geht, die dann um 2 größer ist und dann zu der um 3 größer."},
        {"id": "r3t4", "title": "Lösung", "text": "MUNICHRAPE ist die Lösung"}
        ]
    },
    {
    'title': 'Hauptgang A',
    'datetime': datetime(2017, 6, 21, 19, 0),
    'color': '#ffaa7f',
    'puzzles': [
        {"id": "r4t1", "title": "Tipp 1", "text": "Schaut euch mal die Strahlen auf der alten Karte genauer an. Jeder trägt eine Nummer."},
        {"id": "r4t2", "title": "Tipp 2", "text": "Die grünen Zahlen beschreiben Polarkoordinaten. 3 ist der Radius, 2 der Winkel (also 2. Strahl)"},
        {"id": "r4t3", "title": "Tipp 3", "text": "Der Radius beschreibt vom Schloss aus die so und so vielte Kreuzung"},
        {"id": "r4t4", "title": "Tipp 4", "text": "Was befindet sich heute bei der Kirche links von der Mitte?"},
        {"id": "r4t5", "title": "Lösung", "text": "Lammstraße zwischen Karstadt und Technischem Rathaus ist die Lösung"}
        ]
    },
    {
    'title': 'Hauptgang B',
    'datetime': datetime(2017, 6, 21, 19, 0),
    'color': '#55aa00',
    'puzzles': [
        {"id": "r5t1", "title": "Tipp 1", "text": "Die gefaltete Ecke ist oben links."},
        {"id": "r5t2", "title": "Tipp 2", "text": "Könnt ihr die Karten passend zusammenlegen?"},
        {"id": "r5t3", "title": "Tipp 3", "text": "Die Zeichen sind an den Kanten zu spiegeln - dadurch erkennt ihr, wie sie zusammengehören."},
        {"id": "r5t4", "title": "Tipp 4", "text": "Schaut euch die Kiste auf dem Bild nochmal genauer an!"},
        {"id": "r5t5", "title": "Tipp 5", "text": "Der Code ist Blindenschrift!"},
        {"id": "r5t6", "title": "Lösung", "text": "JA ist die Lösung (zu lesen als J.A.)"}
        ]
    },
    {
    'title': 'Hauptgang C',
    'datetime': datetime(2017, 6, 21, 19, 0),
    'color': '#0047ab',
    'puzzles': [
        {"id": "r6t1", "title": "Tipp 1", "text": "Alle Bilder haben etwas gemeinsam..."},
        {"id": "r6t2", "title": "Tipp 2", "text": "Auf allen Bildern ist ein Typ mit Sonnenbrille zu sehen"},
        {"id": "r6t3", "title": "Tipp 3", "text": "Was ist an dem Typen besonders?"},
        {"id": "r6t4", "title": "Tipp 4", "text": "Vielleicht hat er etwas bei sich?"},
        {"id": "r6t5", "title": "Lösung", "text": 'Er trägt eine Tasche mit der Aufschrift "The Black Pretzels"' }
        ]
    },
    {
    'title': 'Nachspeise',
    'datetime': datetime(2017, 6, 21, 21, 0),
    'color': '#b22222',
    'puzzles': [
        {"id": "r7t1", "title": "Tipp 1", "text": "Öffnet die URL, die ihr als Tipp bekommen habt"},
        {"id": "r7t2", "title": "Tipp 2", "text": "Ihr wisst noch nicht, was MUNICHRAPE bedeutet, oder?"},
        {"id": "r7t3", "title": "Tipp 3", "text": "Geht durch den Mailverlauf und Chatverlauf"},
        {"id": "r7t4", "title": "Tipp 4", "text": "Am Ende braucht ihr noch einmal das Ergebnis des S-Bahn-Rätsels von der Vorspeise. Das war Mathystraße. Jetzt müsst ihr damit wieder etwas machen. Schnappt euch den aktuellen KVV Netzplan (https://www.kvv.de/fileadmin/user_upload/kvv/dokumente/netz/liniennetz/2017/2016-12_L0SCHI_WEB.pdf) und rätselt weiter. Begebt euch dann zu diesem Ort und schaut nach weitere Hinweisen. Mehr verraten wir euch nicht ;)"}
        ]
    }
]
