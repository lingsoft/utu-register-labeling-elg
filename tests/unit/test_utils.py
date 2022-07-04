import unittest
import os

from app.utils import basic_tokenize
from app.utils import full_register_name


class TestBasicTokenizer(unittest.TestCase):
    
    def setUp(self):
        self.fi_text = "Tämä on testi."
        self.empty = ""
        self.long_token = "?" * 200
        self.long_text = "Long set. " * 200
        self.spec_chars = "\N{grinning face}\u4e01\u0009" + self.fi_text + "\u0008"
        self.wrong_lang = "使用人口について正確な統計はないが、日本国内の人口、"

    def test_tokenizer_number_of_tokens(self):
        tokens = basic_tokenize(self.fi_text)
        self.assertEqual(len(tokens), 4)

    def test_tokenizer_empty_string(self):
        tokens = basic_tokenize(self.empty)
        self.assertEqual(len(tokens), 0)

    def test_tokenizer_long_token(self):
        tokens = basic_tokenize(self.long_token)
        self.assertEqual(len(tokens), 200)

    def test_tokenizer_long_text(self):
        tokens = basic_tokenize(self.long_text)
        self.assertGreater(len(tokens), 512)

    def test_tokenizer_special_characters(self):
        tokens = basic_tokenize(self.spec_chars)
        self.assertEqual(len(tokens), 6)

    def test_tokenizer_wrong_language(self):
        tokens = basic_tokenize(self.wrong_lang)
        self.assertEqual(len(tokens), 4)


class TestRegisterNames(unittest.TestCase):

    def test_registers_correct(self):
        label = "NA"
        label, name = full_register_name(label)
        self.assertEqual(name, "Narrative")

    def test_registers_wrong_label(self):
        label = "xx"
        label, name = full_register_name(label)
        self.assertEqual(name, "Unknown")

    def test_registers_none(self):
        label = None
        label, name = full_register_name(label)
        self.assertEqual(name, "Unknown")


if __name__ == "__main__":
    unittest.main()
