import unittest
import os

from app.utils import basic_tokenize


class TestUtils(unittest.TestCase):
    
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


if __name__ == "__main__":
    unittest.main()
