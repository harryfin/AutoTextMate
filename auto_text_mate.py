import time

import keyboard

typed_chars = ''  # Puffer für die zuletzt eingegebenen Zeichen

# Definition der Textbausteine (Auf Joplin-Notizen (Markdown) angepasst)
Daily_Notes = """
# Daily Notes - {}

## Tagesziele
- [ ] Tagziel 1
Tagziel 2
Tagziel 3

## Aufgaben
- [ ] Aufgabe 1
Aufgabe 2
Aufgabe 3
"""

Meeting_Notes = """

# Meetingtype - {}

Meeting Details

## Teilnehmer
- Name 1
Name 2

## Agenda
1. Punkt 1
Punkt 2
Punkt 3


## Protokoll
### Punkt 1
- Information 1
Information 2


### Punkt 2
- Information 1
Information 2

## Aufgaben
- [ ] Aufgabe 1
Aufgabe 2
Aufgabe 3

## Zusammenfassung
**Hauptentscheidungen**:
- Entscheidung 1
Entscheidung 2


**Nächste Schritte**:
- Schritt 1: [Verantwortlich: Name, Fälligkeitsdatum]
Schritt 2: [Verantwortlich: Name, Fälligkeitsdatum]


## Nächstes Meeting
**Datum/Uhrzeit**: [Datum und Uhrzeit des nächsten Meetings]
**Agenda-Vorschläge**:
- Vorschlag 1
Vorschlag 2
"""

# Definition der Ersetzungen
replacements = {
    "#daily": Daily_Notes.format(time.strftime("%d-%m-%Y")),
    "#meeting": Meeting_Notes.format(time.strftime("%d-%m-%Y")),
}

max_trigger_length = max(len(trigger_word) for trigger_word in replacements.keys())


def on_key_event(e):
    global typed_chars
    if e.event_type == 'down':
        if e.name == 'backspace':
            typed_chars = typed_chars[:-1]
        elif e.name == 'space':
            typed_chars += ' '
        elif e.name == 'enter':
            typed_chars += '\n'
        elif len(e.name) == 1:
            typed_chars += e.name
        else:
            # Andere Tasten ignorieren
            pass

        # Puffer auf maximale Schlüsselwortlänge beschränken
        typed_chars = typed_chars[-max_trigger_length:]

        # Überprüfen auf alle Schlüsselwörter
        for trigger_word, replacement_text in replacements.items():
            if typed_chars.endswith(trigger_word):
                # Anzahl der zu löschenden Zeichen
                num_backspaces = len(trigger_word)
                # Lösche das Auslöser-Wort
                for _ in range(num_backspaces):
                    keyboard.press_and_release('backspace')
                # Schreibe den Ersetzungstext
                keyboard.write(replacement_text)
                # Puffer leeren, um Seiteneffekte zu vermeiden
                typed_chars = ""
                break  # Nach erster Übereinstimmung abbrechen


if __name__ == "__main__":
    # Registrieren des Hooks
    keyboard.hook(on_key_event)

    # Skript läuft kontinuierlich
    keyboard.wait()
