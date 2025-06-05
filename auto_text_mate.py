import datetime
from pathlib import Path
import keyboard
import tkinter as tk
from tkinter import messagebox
import logging
import sys
from typing import Dict, Tuple
import pathlib
import re

SHOW_NOTES_TRIGGER = "§§show-notes"
EXIT_TRIGGER = "§§exit"

root_path = pathlib.Path(__file__).parent.absolute()

# Configure logging
logging.basicConfig(
    filename=root_path / 'note_replacer.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def read_file(file_path: str) -> str:
    """Reads the content of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The content of the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as ex:
        logging.error(f"Error reading file {file_path}: {ex}")
        return ""

def load_notes(directory: str) -> Dict[str, str]:
    """Loads notes from a directory.

    Args:
        directory (str): The path to the directory containing notes.

    Returns:
        Dict[str, str]: A dictionary mapping trigger words to note contents.
    """
    notes = {}
    directory_path = Path(directory)
    if not directory_path.exists():
        logging.warning(f"Notes directory {directory} does not exist.")
        return notes

    for file_path in directory_path.glob('*.txt'):
        trigger_word = f"§§{file_path.stem}"
        notes[trigger_word] = read_file(file_path)
    return notes

def get_template_date() -> Dict[str, str]:
    """Returns today's date and the upcoming week's number.

    This helper keeps backwards compatibility with older notes that rely on
    ``{date}`` and ``{kw}`` placeholders.
    """

    today = datetime.date.today()
    upcoming_monday = today + datetime.timedelta(days=(0 - today.weekday()) % 7)
    kw = upcoming_monday.isocalendar()[1]
    return {"date": today.strftime("%d-%m-%Y"), "kw": str(kw)}


def _compute_upcoming_weekday(day_index: int, weeks_offset: int = 0) -> datetime.date:
    """Returns the next occurrence of the given weekday.

    The returned date is ``today`` if the weekday matches ``today``. ``weeks_offset``
    shifts the result by whole weeks.
    """

    today = datetime.date.today()
    delta = (day_index - today.weekday()) % 7
    base = today + datetime.timedelta(days=delta)
    return base + datetime.timedelta(weeks=weeks_offset)


def fill_template(template_text: str) -> str:
    """Replace date placeholders in ``template_text`` with computed values."""

    days = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }

    today = datetime.date.today()

    def repl(match: re.Match) -> str:
        token = match.group(1)
        base, sep, offset_str = token.partition("+")
        offset = int(offset_str) if sep else 0

        key = base.lower()
        if key == "date":
            return (today + datetime.timedelta(days=offset)).strftime("%d-%m-%Y")
        if key == "kw":
            monday = _compute_upcoming_weekday(0, offset)
            return str(monday.isocalendar()[1])
        if key in days:
            day_date = _compute_upcoming_weekday(days[key], offset)
            return day_date.strftime("%Y-%m-%d")

        return match.group(0)

    return re.sub(r"{([^{}]+)}", repl, template_text)

def setup_replacements() -> Tuple[Dict[str, str], int]:
    """Sets up the replacements dictionary and calculates the maximum trigger length.

    Returns:
        Tuple[Dict[str, str], int]: A tuple containing the replacements dictionary and the maximum trigger length.
    """
    try:
        script_directory = Path(__file__).parent
        notes_directory = script_directory / 'notes'
        replacements = load_notes(str(notes_directory))
        max_trigger_length = max(
            [len(trigger_word) for trigger_word in replacements.keys()] + [len(SHOW_NOTES_TRIGGER), len(EXIT_TRIGGER)]
        )
        return replacements, max_trigger_length
    except Exception as ex:
        logging.error(f"Error initializing script: {ex}")
        return {}, 0

def on_key_event(event: keyboard.KeyboardEvent, typed_chars: str, replacements: Dict[str, str], max_trigger_length: int) -> str:
    """Handles key events and updates the typed characters.

    Args:
        event (keyboard.KeyboardEvent): The keyboard event.
        typed_chars (str): The current typed characters.
        replacements (Dict[str, str]): The replacements dictionary.
        max_trigger_length (int): The maximum trigger length.

    Returns:
        str: The updated typed characters.
    """
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

def show_notes_window(note_names: list) -> None:
    """Displays a window with the list of note names.

    Args:
        note_names (list): The list of note names.
    """
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        note_list = "\n".join(note_names)
        messagebox.showinfo("Notes", note_list)
        root.destroy()  # Destroy the root window after showing the message box
    except Exception as ex:
        logging.error(f"Error displaying notes window: {ex}")


def check_and_replace(typed_chars: str, replacements: Dict[str, str]) -> str:
    """Checks for trigger words and replaces them with the corresponding text.

    Args:
        typed_chars (str): The current typed characters.
        replacements (Dict[str, str]): The replacements dictionary.

    Returns:
        str: The updated typed characters.
    """
    try:
        for trigger_word, template_text in replacements.items():
            if typed_chars.strip().endswith(trigger_word):
                logging.info(f"Trigger word found: {trigger_word}")
                num_backspaces = len(trigger_word) + 1
                # Delete the trigger word
                for _ in range(num_backspaces):
                    keyboard.press_and_release('backspace')

                replacement_text = fill_template(template_text)
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

def main() -> None:
    """Main function to start the script."""
    replacements, max_trigger_length = setup_replacements()
    typed_chars = ""

    def key_event_handler(event: keyboard.KeyboardEvent) -> None:
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