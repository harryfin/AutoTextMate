import logging
import unittest
from pathlib import Path
from unittest.mock import patch, mock_open
import sys
import types

if 'keyboard' not in sys.modules:
    stub = types.SimpleNamespace(
        press_and_release=lambda *a, **k: None,
        write=lambda *a, **k: None,
        hook=lambda *a, **k: None,
        wait=lambda *a, **k: None,
        unhook_all=lambda *a, **k: None,
        KeyboardEvent=object,
    )
    sys.modules['keyboard'] = stub

from auto_text_mate import read_file, load_notes, get_template_date, check_and_replace, fill_template


class TestAutoTextMate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)

    @patch('builtins.open', new_callable=mock_open, read_data='note content')
    def test_reads_file_content(self, mock_file):
        result = read_file('dummy_path')
        self.assertEqual(result, 'note content')

    @patch('auto_text_mate.Path.exists', return_value=True)
    @patch('auto_text_mate.Path.glob', return_value=[Path('test.txt')])
    @patch('auto_text_mate.read_file', return_value='note content')
    def test_loads_notes_from_directory(self, mock_read_file, mock_glob, mock_exists):
        result = load_notes('dummy_directory')
        self.assertEqual(result, {'§§test': 'note content'})

    @patch('auto_text_mate.Path.exists', return_value=False)
    def test_returns_empty_dict_if_directory_not_exists(self, mock_exists):
        result = load_notes('dummy_directory')
        self.assertEqual(result, {})

    def test_gets_current_date_and_week_number(self):
        result = get_template_date()
        self.assertIn('date', result)
        self.assertIn('kw', result)

    @patch('auto_text_mate.keyboard.press_and_release')
    @patch('auto_text_mate.keyboard.write')
    @patch('auto_text_mate.fill_template', return_value='note content 01-01-2023 1')
    def test_replaces_trigger_word_with_template_text(self, mock_fill_template, mock_write, mock_press_and_release):
        replacements = {'§§test': 'note content {date} {kw}'}
        result = check_and_replace('§§test', replacements)
        mock_press_and_release.assert_called_with('backspace')
        mock_write.assert_called_with('note content 01-01-2023 1')
        mock_fill_template.assert_called_once_with('note content {date} {kw}')
        self.assertEqual(result, '')

    @patch('auto_text_mate.tk.Tk')
    @patch('auto_text_mate.tk.messagebox.showinfo')
    def test_shows_notes_window_on_show_notes_trigger(self, mock_showinfo, mock_tk):
        replacements = {'§§test': 'note content'}
        result = check_and_replace('§§show-notes', replacements)
        mock_showinfo.assert_called_once_with("Notes", "§§test")
        self.assertEqual(result, '')


if __name__ == '__main__':
    unittest.main()
