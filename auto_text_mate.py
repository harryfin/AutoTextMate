import datetime
from pathlib import Path
import keyboard
import tkinter as tk
from tkinter import messagebox
import logging
import sys

SHOW_NOTES_TRIGGER = "#show-notes"
EXIT_TRIGGER = "#exit"

# Configure logging
logging.basicConfig(
    filename='note_replacer.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as ex:
        logging.error(f"Error reading file {file_path}: {ex}")
        return ""

def load_notes(directory):
    notes = {}
    directory_path = Path(directory)
    if not directory_path.exists():
        logging.warning(f"Notes directory {directory} does not exist.")
        return notes

    for file_path in directory_path.glob('*_notes.txt'):
        trigger_word = f"#{file_path.stem.split('_')[0]}"
        notes[trigger_word] = read_file(file_path)
    return notes

def get_template_date() -> dict:
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    kw = datetime.datetime.now().isocalendar()[1]
    return {"date": date, "kw": kw}

def setup_replacements():
    try:
        script_directory = Path(__file__).parent
        notes_directory = script_directory / 'notes'
        replacements = load_notes(notes_directory)
        max_trigger_length = max(
            (len(trigger_word) for trigger_word in replacements.keys()),
            default=max(len(SHOW_NOTES_TRIGGER), len(EXIT_TRIGGER))
        )
        return replacements, max_trigger_length
    except Exception as ex:
        logging.error(f"Error initializing script: {ex}")
        return {}, 0

def on_key_event(event, typed_chars, replacements, max_trigger_length):
    try:
        if event.event_type == 'down':
            if event.name == 'backspace':
                typed_chars = typed_chars[:-1]
            elif event.name == 'space':
                typed_chars += ' '
                typed_chars = check_and_replace(typed_chars, replacements)
            elif event.name == 'enter':
                typed_chars += '\n'
                typed_chars = check_and_replace(typed_chars, replacements)
            elif len(event.name) == 1:
                typed_chars += event.name
            else:
                pass

            typed_chars = typed_chars[-(max_trigger_length + 1):]
    except Exception as ex:
        logging.error(f"Error processing key event: {ex}")
    return typed_chars

def show_notes_window(note_names):
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        note_list = "\n".join(note_names)
        messagebox.showinfo("Notes", note_list)
        root.after(0, root.destroy)  # Schedule the destruction of the root window
        root.mainloop()
    except Exception as ex:
        logging.error(f"Error displaying notes window: {ex}")

def check_and_replace(typed_chars, replacements):
    try:
        for trigger_word, template_text in replacements.items():
            if typed_chars.strip().endswith(trigger_word):
                logging.info(f"Trigger word found: {trigger_word}")
                num_backspaces = len(trigger_word) + 1
                # Delete the trigger word
                for _ in range(num_backspaces):
                    keyboard.press_and_release('backspace')

                template_data = get_template_date()
                replacement_text = template_text.format(**template_data)
                keyboard.write(replacement_text)
                return ""

        if typed_chars.strip().endswith(SHOW_NOTES_TRIGGER):
            logging.info(f"Call to show notes window. [{typed_chars.strip()}]")
            note_names = list(replacements.keys())
            show_notes_window(note_names)
            return ""

        if typed_chars.strip().endswith(EXIT_TRIGGER):
            logging.info(f"Call to exit the script. [{typed_chars.strip()}]")
            keyboard.unhook_all()
            logging.info("Script stopped.")
            sys.exit(0)

    except Exception as ex:
        logging.error(f"Error in check_and_replace: {ex}")
    return typed_chars

def main():
    replacements, max_trigger_length = setup_replacements()
    typed_chars = ""

    def key_event_handler(event):
        nonlocal typed_chars
        typed_chars = on_key_event(event, typed_chars, replacements, max_trigger_length)

    try:
        keyboard.hook(key_event_handler)
        logging.info("Script started successfully.")
        keyboard.wait()
    except Exception as ex:
        logging.error(f"Error in main execution: {ex}")

if __name__ == "__main__":
    main()