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


def call_api(payload):
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps(payload)
    return  requests.post(
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
        self.assertEqual(len(response.get("classes")), 24)

    def test_api_response_with_empty_text(self):
        payload = create_payload("")
        response = call_api(payload)["response"]
        self.assertIn("classes", response)

    def test_api_response_with_too_long_text(self):
        # TODO FAIL Internal error
        long_text = "Long set. " * 200
        payload = create_payload(long_text)
        response = call_api(payload)
        self.assertEqual(response['failure']['errors'][0]['code'],
                         'elg.request.too.large')

    def test_api_response_with_long_token(self):
        # TODO Failure (give own error message)
        long_token = "å" * 2000
        payload = create_payload(long_token)
        response = call_api(payload)
        self.assertIn("classes", response)

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


if __name__ == '__main__':
    unittest.main()
