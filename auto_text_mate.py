import time
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
    # Check for all trigger words
    for trigger_word, template_text in replacements.items():
        if typed_chars.strip().endswith(trigger_word):
            # Number of characters to delete
            num_backspaces = len(trigger_word +1)  # +1 for the hashtag
            # Delete the trigger word
            for _ in range(num_backspaces):
                keyboard.press_and_release('backspace')
            # Write the replacement text with the current date
            replacement_text = template_text.format(time.strftime("%d-%m-%Y"))
            keyboard.write(replacement_text)
            # Clear the buffer to avoid side effects
            typed_chars = ""
            break  # Stop after the first match

if __name__ == "__main__":
    # Register the hook
    keyboard.hook(on_key_event)

    # Script runs continuously
    keyboard.wait()