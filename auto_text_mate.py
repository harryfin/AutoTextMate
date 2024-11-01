from pathlib import Path
import time

import keyboard

typed_chars = ''  # Puffer für die zuletzt eingegebenen Zeichen


# Funktion zum Lesen einer Textdatei
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


# Funktion zum Laden aller Textbausteine aus einem Verzeichnis
def load_notes(directory):
    notes = {}
    directory_path = Path(directory)
    for file_path in directory_path.iterdir():
        if file_path.is_file() and file_path.name.endswith('_notes.txt'):
            trigger_word = f"#{file_path.stem.split('_')[0]}"
            notes[trigger_word] = read_file(file_path)
    return notes


# Verzeichnis der Textbausteine relativ zum Skriptverzeichnis
script_directory = Path(__file__).parent
notes_directory = script_directory / 'notes'

replacements = load_notes(notes_directory)

# Berechnung der maximalen Schlüsselwortlänge
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
        for trigger_word, template_text in replacements.items():
            if typed_chars.endswith(trigger_word):
                # Anzahl der zu löschenden Zeichen
                num_backspaces = len(trigger_word)
                # Lösche das Auslöser-Wort
                for _ in range(num_backspaces):
                    keyboard.press_and_release('backspace')
                # Schreibe den Ersetzungstext mit aktuellem Datum
                replacement_text = template_text.format(time.strftime("%d-%m-%Y"))
                keyboard.write(replacement_text)
                # Puffer leeren, um Seiteneffekte zu vermeiden
                typed_chars = ""
                break  # Nach erster Übereinstimmung abbrechen


if __name__ == "__main__":
    # Registrieren des Hooks
    keyboard.hook(on_key_event)

    # Skript läuft kontinuierlich
    keyboard.wait()
