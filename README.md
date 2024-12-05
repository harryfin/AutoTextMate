# AutoTextMate: Automatisches Ersetzen von Textbausteinen in Echtzeit
**AutoTextMate** ist ein einfaches Python-Programm, das es ermöglicht, vordefinierte Textbausteine durch Tastatureingaben automatisch zu ersetzen. Es eignet sich ideal für Nutzer, die häufig bestimmte Texteingaben wiederholen und Zeit sparen möchten, indem sie Kürzel für lange oder komplexe Textblöcke verwenden.

# Funktionen
- Automatisches Ersetzen von Textkürzeln: Ersetzt benutzerdefinierte Kürzel (z.B. #daily, #todo) automatisch mit den entsprechenden Textbausteinen.
- Echtzeitüberwachung der Tastatur: Überwacht die Tastatureingaben und ersetzt Kürzel sofort, nachdem ein Leerzeichen eingegeben wird.
- Datumseinbindung: Automatische Einbindung des aktuellen Datums bei bestimmten Textvorlagen, wie z.B. täglichen Notizen.

# Installation

## 1. Virtuelles Environment erstellen (Windows & Linux)
Es wird empfohlen, ein isoliertes virtuelles Python-Environment zu verwenden, um Konflikte mit anderen Projekten zu vermeiden.

### Windows:
1. Öffne ein Terminal (CMD, PowerShell oder Git Bash) im Projektordner.
2. Erstelle ein virtuelles Environment:
   ```bash
   python -m venv venv
   ```
3. Aktiviere das Environment:
   ```bash
   venv\Scripts\activate
   ```

### Linux/macOS:
1. Öffne ein Terminal im Projektordner.
2. Erstelle ein virtuelles Environment:
   ```bash
   python3 -m venv venv
   ```
3. Aktiviere das Environment:
   ```bash
   source venv/bin/activate
   ```

## 2. Abhängigkeiten installieren:
Stelle sicher, dass die erforderlichen Python-Bibliotheken installiert sind. Dies wird nun innerhalb des virtuellen Environments ausgeführt:

```bash
pip install -r requirements.txt
```

## 3. Code herunterladen:
Lade den Quellcode herunter oder klone das Repository:

```bash
git clone https://github.com/harryfin/AutoTextMate.git
```

## 4. Programm ausführen:
Führe das Programm innerhalb des aktivierten virtuellen Environments aus, um die Überwachung der Tastatur zu starten:

```bash
python auto_text_mate.py
```

## 5. Deaktivierung des virtuellen Environments:
Nach der Ausführung kannst du das virtuelle Environment mit folgendem Befehl deaktivieren:

### Windows:
```bash
venv\Scripts\deactivate
```

### Linux/macOS:
```bash
deactivate
```


# Nutzung

1. Anlegen von Textbausteinen:
   - Legen Sie alle Textbausteine in dem Verzeichnis `notes/` ab.
   - Benennen Sie die Dateien nach dem Muster `triggerword_notes.txt`, z.B. `daily_notes.txt`, `meeting_notes.txt`.


2. Textkürzel verwenden:
Sobald das Programm läuft, kannst du die definierten Kürzel (z.B. #daily) in jedem beliebigen Textfeld eingeben. Nach der Eingabe des Kürzels und Drücken der Leertaste wird das Kürzel automatisch durch den zugehörigen Text ersetzt.

# Beispiel
Wenn du das Kürzel `#daily` eingibst, wird es durch Folgendes ersetzt (mit dem aktuellen Datum):

````markdown
# Daily Notes - 05-09-2024

## Tagesziele
- [ ] Tagziel 1
- [ ] Tagziel 2
- [ ] Tagziel 3

## Aufgaben
- [ ] Aufgabe 1
- [ ] Aufgabe 2
- [ ] Aufgabe 3
````


# Autostart mit Batch-Datei mit virtuellem Environment
## Windows
Du kannst auch eine Batch-Datei erstellen, die zuerst das virtuelle Environment aktiviert und dann das Skript ausführt.

Erstelle eine .bat-Datei von start_auto_text_mate.bat.example, die folgendes enthält:

````batch
@echo off
C:\path\to\venv\Scripts\python.exe C:\path\to\your_script.py
````

oder eine .vbs-Datei von start_auto_text_mate.vbs.example, die folgendes enthält:

````vbs
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "C:\path\to\venv\Scripts\pythonw.exe C:\path\to\your_script.py", 0
Set WshShell = Nothing
````

Parameter:
- 0: Das Fenster wird nicht angezeigt.

Lege diese Datei in den Autostart-Ordner (Win + R → shell:startup).


## Ausführung des Skriptes mit Docker

### Schritte

1. **Docker-Image bauen**  
   ```bash
   docker build -t auto-text-mate .
   ```

2. **Skript ohne Internet ausführen**  
   ```bash
   docker run --rm --network none auto-text-mate
   ```

### Vorteile
- **Sicherheit**: Kein Internetzugriff.
- **Reproduzierbarkeit**: Einheitliche Umgebung.

#conda 

#conda 