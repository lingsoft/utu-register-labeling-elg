import unittest
import os
import requests
import json


API_URL = 'http://localhost:8000/process'


def read_fixture(fname):
    fixture_path = "tests/integration/fixtures/"
    with open(os.path.join(fixture_path, fname)) as infile:
        return infile.read()


def create_payload(text):
    return {"type": "text", "content": text}


def create_payload_with_params(text, params):
    return {"type": "text", "content": text, "params": params}


def call_api(payload):
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps(payload)
    return requests.post(
            API_URL, headers=headers, data=payload).json()


class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.steady_text = "Tämä on testi."

    def test_api_response_type(self):
        payload = create_payload(self.steady_text)
        response = call_api(payload)["response"]
        self.assertEqual(response.get("type"), "classification")

    def test_api_response_content(self):
        payload = create_payload(self.steady_text)
        response = call_api(payload)["response"]
        # Should return at least one class with threshold 0.4
        self.assertGreater(len(response.get("classes")), 0)

    def test_api_response_class_names(self):
        payload = create_payload(self.steady_text)
        response = call_api(payload)["response"]
        self.assertEqual(len(response["classes"][0]["class"].split("-")), 2)

    def test_api_response_with_empty_text(self):
        payload = create_payload("")
        response = call_api(payload)["response"]
        self.assertIn("classes", response)

    def test_api_response_with_too_long_text(self):
        long_text = "Long set. " * 200
        payload = create_payload(long_text)
        response = call_api(payload)
        self.assertEqual(response["failure"]["errors"][0]["code"],
                         "lingsoft.token.too.many")

    def test_api_response_with_long_token(self):
        long_token = "å" * 101
        payload = create_payload(long_token)
        response = call_api(payload)
        self.assertEqual(response["failure"]["errors"][0]["code"],
                         "lingsoft.token.too.long")

    def test_api_response_with_special_characters(self):
        spec_text = "\N{grinning face}\u4e01\u0009" + self.steady_text + "\u0008"
        payload = create_payload(spec_text)
        response = call_api(payload)["response"]
        self.assertIn("classes", response)

    def test_api_response_with_unsupported_language(self):
        wrong_lang = "使用人口について正確な統計はないが、日本国内の人口、"
        payload = create_payload(wrong_lang)
        response = call_api(payload)["response"]
        self.assertIn("classes", response)

    def test_api_response_with_valid_parameters(self):
        params = {"threshold": 0.2, "sub_registers": False}
        payload = create_payload_with_params(self.steady_text, params)
        response = call_api(payload)["response"]
        self.assertNotIn("warnings", response)

    def test_api_response_with_none_threshold(self):
        params = {"threshold": None}
        payload = create_payload_with_params(self.steady_text, params)
        response = call_api(payload)["response"]
        self.assertEqual(response["warnings"][0]["code"],
                         "lingsoft.params.invalid.type")

    def test_api_response_with_invalid_threshold(self):
        params = {"threshold": 1.1}
        payload = create_payload_with_params(self.steady_text, params)
        response = call_api(payload)["response"]
        self.assertEqual(response["warnings"][0]["code"],
                         "lingsoft.params.invalid.value")

    def test_api_response_with_invalid_sub_registers(self):
        params = {"sub_registers": "False"}
        payload = create_payload_with_params(self.steady_text, params)
        response = call_api(payload)["response"]
        self.assertEqual(response["warnings"][0]["code"],
                         "lingsoft.params.invalid.type")

    def test_api_response_with_invalid_parameters(self):
        params = {"threshold": [], "sub_registers": "False"}
        payload = create_payload_with_params(self.steady_text, params)
        response = call_api(payload)["response"]
        self.assertEqual(len(response["warnings"]), 2)

    def test_api_response_with_general_registers(self):
        params = {"threshold": "-0.6", "sub_registers": "False"}
        payload = create_payload_with_params(self.steady_text, params)
        response = call_api(payload)["response"]
        self.assertEqual(len(response["classes"]), 8)

    def test_api_response_with_empty_params(self):
        params = {}
        payload = create_payload_with_params(self.steady_text, params)
        response = call_api(payload)["response"]
        self.assertGreater(len(response.get("classes")), 0)


if __name__ == '__main__':
    unittest.main()
