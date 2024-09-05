import pyautogui
import keyboard
import time


# Definition der Textbausteine
Daily_Notes = """
#Daily Notes - {}

## Tagesziele
- [ ]
- [ ] 
- [ ]

## Aufgaben
- [ ] 
- [ ]
- [ ]
"""


texts = {
    "#daily": Daily_Notes.format(time.strftime("%d-%m-%Y")),
    "#todo": "1. Aufgabe\n2. Aufgabe\n3. Aufgabe",
    "#meeting": "Besprechung am Montag um 10 Uhr.",
}

# Funktion, um Text zu ersetzen
def replace_text(typed_text, replacement_text):
    # Lösche das getippte Kürzel (z.B. #todo)
    for _ in range(len(typed_text)):
        pyautogui.press('backspace')
    # Schreibe den neuen Text
    pyautogui.write(replacement_text)

# Überwache die Tastatureingaben
def monitor_input():
    buffer = ""  # Buffer, um eingegebene Zeichen zu speichern
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'space':
                # Wenn eine Leertaste gedrückt wird, prüfe, ob ein Kürzel im Buffer ist
                if buffer in texts:
                    replace_text(buffer, texts[buffer])
                buffer = ""  # Leere den Buffer nach einem Leerzeichen
            elif event.name == 'backspace':
                buffer = buffer[:-1]  # Entferne das letzte Zeichen aus dem Buffer
            elif len(event.name) == 1:  # Normale Zeichen wie a-z
                buffer += event.name

# Starte die Überwachung
if __name__ == "__main__":
    print("Überwache die Eingabe für Schlüsselwörter...")
    monitor_input()

