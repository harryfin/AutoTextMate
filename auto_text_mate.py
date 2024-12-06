import tkinter as tk
import datetime
from pathlib import Path

import keyboard

typed_chars = ''  # Buffer for the last typed characters


# Function to read a text file
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


# Function to load all text snippets from a directory
def load_notes(directory):
    notes = {}
    directory_path = Path(directory)
    for file_path in directory_path.iterdir():
        if file_path.is_file() and file_path.name.endswith('_notes.txt'):
            trigger_word = f"#{file_path.stem.split('_')[0]}"
            notes[trigger_word] = read_file(file_path)
    return notes


def get_template_date() -> dict:
    """
    Returns template data with following keys:
    - date: Current date in the format dd-mm-YYYY
    - kw: Calendar week of the current date

    Returns:
        dict: Dictionary with the current date and calendar week

    """
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    kw = datetime.datetime.now().isocalendar()[1]
    return {"date": date, "kw": kw}


def show_all_notes(notes):
    """
    Opens a temporary window to display all available notes.
    """
    root = tk.Tk()
    root.title("All Notes")

    # Add a scrollbar
    scrollbar = tk.Scrollbar(root)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Add a Text widget to display notes
    text = tk.Text(root, wrap=tk.WORD, yscrollcommand=scrollbar.set)
    text.pack(expand=True, fill=tk.BOTH)

    # Populate the Text widget with all notes
    for trigger_word, note_content in notes.items():
        text.insert(tk.END, f"{trigger_word}:\n{note_content}\n{'-'*40}\n")

    # Configure the scrollbar
    scrollbar.config(command=text.yview)

    # Run the Tkinter event loop
    root.mainloop()


# Directory of text snippets relative to the script directory
script_directory = Path(__file__).parent
notes_directory = script_directory / 'notes'

replacements = load_notes(notes_directory)

# Calculate the maximum trigger word length
max_trigger_length = max(len(trigger_word) for trigger_word in replacements.keys())


def on_key_event(e):
    global typed_chars
    if e.event_type == 'down':
        if e.name == 'backspace':
            typed_chars = typed_chars[:-1]
        elif e.name == 'space':
            typed_chars += ' '
            check_and_replace()
        elif e.name == 'enter':
            typed_chars += '\n'
            check_and_replace()
        elif len(e.name) == 1:
            typed_chars += e.name
        else:
            # Ignore other keys
            pass

        # Limit the buffer to the maximum trigger word length plus one for the space or enter
        typed_chars = typed_chars[-(max_trigger_length + 1):]


def check_and_replace():
    global typed_chars
    # Check for the special trigger "#all_notes"
    if typed_chars.strip().endswith("#all_notes"):
        # Delete the trigger word
        num_backspaces = len("#all_notes") + 1  # +1 for the hashtag
        for _ in range(num_backspaces):
            keyboard.press_and_release('backspace')

        # Show all notes in a temporary window
        show_all_notes(replacements)

        # Clear the buffer
        typed_chars = ""
        return

    # Check for other trigger words
    for trigger_word, template_text in replacements.items():
        if typed_chars.strip().endswith(trigger_word):
            # Number of characters to delete
            num_backspaces = len(trigger_word) + 1  # +1 for the hashtag
            # Delete the trigger word
            for _ in range(num_backspaces):
                keyboard.press_and_release('backspace')

            template_data = get_template_date()  # Get the current date and calendar week
            replacement_text = template_text.format(**template_data)
            keyboard.write(replacement_text)
            # Clear the buffer to avoid side effects
            typed_chars = ""
            break  # Stop after the first match


if __name__ == "__main__":
    # Register the hook
    keyboard.hook(on_key_event)

    # Script runs continuously
    keyboard.wait()

