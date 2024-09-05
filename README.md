# AutoTextMate: Automatisches Ersetzen von Textbausteinen in Echtzeit
**AutoTextMate** ist ein einfaches Python-Programm, das es ermöglicht, vordefinierte Textbausteine durch Tastatureingaben automatisch zu ersetzen. Es eignet sich ideal für Nutzer, die häufig bestimmte Texteingaben wiederholen und Zeit sparen möchten, indem sie Kürzel für lange oder komplexe Textblöcke verwenden.

# Funktionen
- Automatisches Ersetzen von Textkürzeln: Ersetzt benutzerdefinierte Kürzel (z.B. #daily, #todo) automatisch mit den entsprechenden Textbausteinen.
- Echtzeitüberwachung der Tastatur: Überwacht die Tastatureingaben und ersetzt Kürzel sofort, nachdem ein Leerzeichen eingegeben wird.
- Datumseinbindung: Automatische Einbindung des aktuellen Datums bei bestimmten Textvorlagen, wie z.B. täglichen Notizen.
- Verwendung der Zwischenablage: Schnelles und fehlerfreies Einfügen von Text durch Kopieren in die Zwischenablage und anschließendes Einfügen mit der Tastenkombination STRG+V.
# Installation
1. Abhängigkeiten installieren:

Stelle sicher, dass die folgenden Python-Bibliotheken installiert sind:

```bash
pip install pyautogui keyboard pyperclip
```
2. Code herunterladen:

Lade den Quellcode herunter oder klone das Repository:

```bash
git clone https://github.com/harryfin/AutoTextMate.git
```

2. Programm ausführen:

Führe das Programm aus, um die Überwachung der Tastatur zu starten:

```bash
python auto_text_mate.py
```

# Nutzung
1. Definiere deine Textbausteine:
Du kannst im Dictionary texts Kürzel wie #daily, #todo oder #meeting definieren, die dann durch den zugehörigen Text ersetzt werden.

Beispiel:

```python
texts = {
    "#daily": "...",
    "#todo": "...",
    "#meeting": "...",
}

```
2. Textkürzel verwenden:
Sobald das Programm läuft, kannst du die definierten Kürzel (z.B. #daily) in jedem beliebigen Textfeld eingeben. Nach der Eingabe des Kürzels und Drücken der Leertaste wird das Kürzel automatisch durch den zugehörigen Text ersetzt.

# Beispiel
Wenn du das Kürzel `#daily` eingibst, wird es durch Folgendes ersetzt (mit dem aktuellen Datum):

````markdown
# Daily Notes - 05-09-2024

## Tagesziele
- [ ]
- [ ] 
- [ ]

## Aufgaben
- [ ] 
- [ ]
- [ ]
````
