import unittest
import os

from app.ttml.predict import load_models, predict


model_dir = "app/ttml/models"
tok_name = os.path.join(model_dir, "xlm-roberta-base")
fine_tuned = os.path.join(model_dir, "xlmr-base-en-fi-fr-se.pt")
tokenizer, model = load_models(tok_name, fine_tuned)
N_LABELS = 24


class TestPredict(unittest.TestCase):
    
    def setUp(self):
        self.fi_text = "Tämä on testi."
        self.empty = ""
        self.long_token = "å" * 2000
        self.long_text = "Long set. " * 200
        self.spec_chars = "\N{grinning face}\u4e01\u0009" + self.fi_text + "\u0008"
        self.wrong_lang = "使用人口について正確な統計はないが、日本国内の人口、"

    def test_model_loading_failure(self):
        with self.assertRaises(OSError):
            tokenizer, model = load_models("abc", "def")

    def test_number_of_labels(self):
        probs = predict(tokenizer, model, self.fi_text)
        self.assertEqual(len(probs), N_LABELS)

    def test_empty_string(self):
        probs = predict(tokenizer, model, self.empty)
        self.assertEqual(len(probs), N_LABELS)

    def test_long_token_failure(self):
        with self.assertRaises(RuntimeError):
            probs = predict(tokenizer, model, self.long_token)

    def test_long_text_failure(self):
        with self.assertRaises(RuntimeError):
            probs = predict(tokenizer, model, self.long_text)

    def test_special_characters(self):
        probs = predict(tokenizer, model, self.spec_chars)
        self.assertEqual(len(probs), N_LABELS)
    
    def test_wrong_language(self):
        probs = predict(tokenizer, model, self.wrong_lang)
        self.assertEqual(len(probs), N_LABELS)


if __name__ == "__main__":
    unittest.main()
