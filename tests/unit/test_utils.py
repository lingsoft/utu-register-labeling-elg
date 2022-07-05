import unittest
import os

from app.utils import basic_tokenize
from app.utils import full_register_name
from app.utils import validate_threshold
from app.utils import validate_sub_registers


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


class TestParameterValidation(unittest.TestCase):

    def setUp(self):
        self.threshold = 0.4
        self.sub_registers = True

    def test_params_sub_registers_valid(self):
        params = {"sub_registers": False}
        sub_registers, warning = validate_sub_registers(
                params, self.sub_registers)
        self.assertFalse(sub_registers)

    def test_params_sub_registers_missing(self):
        params = {"sub_regs": False}
        sub_registers, warning = validate_sub_registers(
                params, self.sub_registers)
        self.assertTrue(sub_registers)

    def test_params_sub_registers_conversion(self):
        params = {"sub_registers": "False"}
        sub_registers, warning = validate_sub_registers(
                params, self.sub_registers)
        self.assertFalse(sub_registers)

    def test_params_sub_registers_with_none(self):
        params = {"sub_registers": None}
        sub_registers, warning = validate_sub_registers(
                params, self.sub_registers)
        self.assertIsNotNone(warning)

    def test_params_sub_registers_with_none(self):
        params = {"sub_registers": 0.4}
        sub_registers, warning = validate_sub_registers(
                params, self.sub_registers)
        self.assertIsNotNone(warning)

    def test_params_threshold_valid(self):
        new_value = 0.6
        params = {"threshold": new_value}
        threshold, warning = validate_threshold(params, self.threshold)
        self.assertEqual(threshold, new_value)

    def test_params_threshold_with_none(self):
        params = {"threshold": None}
        threshold, warning = validate_threshold(params, self.threshold)
        self.assertEqual(threshold, self.threshold)

    def test_params_threshold_missing(self):
        params = {"thres": 0.6}
        threshold, warning = validate_threshold(params, self.threshold)
        self.assertEqual(threshold, self.threshold)

    def test_params_threshold_valid_convertsion(self):
        params = {"threshold": "0.6"}
        threshold, warning = validate_threshold(params, self.threshold)
        self.assertIsNone(warning)

    def test_params_threshold_missing(self):
        params = {"threshold": [0.6]}
        threshold, warning = validate_threshold(params, self.threshold)
        self.assertIsNotNone(warning)

    def test_params_threshold_out_of_bounds(self):
        params = {"threshold": -0.6}
        threshold, warning = validate_threshold(params, self.threshold)
        self.assertIsNotNone(warning)


if __name__ == "__main__":
    unittest.main()
