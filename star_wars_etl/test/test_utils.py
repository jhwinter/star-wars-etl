import json
import unittest
from unittest.mock import Mock

import requests
import responses

from star_wars_etl import utils


class TestUtils(unittest.TestCase):
    def test_remove_none(self):
        a_list = [
            [],
            "blah",
            "",
            "yo",
            0,
            56,
            False,
            True,
            None,
            "testing",
            None,
            {"terry": "tester"}
        ]
        expected_result = [
            [],
            "blah",
            "",
            "yo",
            0,
            56,
            False,
            True,
            "testing",
            {"terry": "tester"}
        ]
        self.assertEqual(utils.remove_none(a_list), expected_result)

    def test_get_json(self):
        a_dict = {
            "blah": "blue",
            "test": "testing",
            "number": 100
        }
        expected_result = json.dumps(a_dict, indent=4, ensure_ascii=False)
        self.assertEqual(utils.get_json(a_dict), expected_result)

    def test_generate_url(self):
        self.assertEqual(
            f"{utils.STAR_WARS_API}/films/23/",
            utils.generate_url("films")(23)
        )

    def test_is_valid_response(self):
        the_response = Mock(spec=requests.models.Response)
        the_response.json.return_value = {"test": "tester"}
        the_response.status_code = 200
        self.assertEqual(
            utils.is_valid_response(the_response),
            the_response.json.return_value
        )

    def test_get_data(self):
        url = utils.generate_url("people")(1)
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, url, json={"test": "tester"}, status=200)
            resp = utils.get_data(url)

        self.assertEqual(resp, {"test": "tester"})

    def test_cm_to_in(self):
        self.assertEqual(utils.cm_to_in(50), 19.68504)

    def test_in_to_ft(self):
        self.assertEqual(utils.in_to_ft(50), 4)

    def test_convert_height(self):
        self.assertEqual(utils.convert_height(170), "5 ft 6.93 in")

    def test_kg_to_lb(self):
        self.assertEqual(utils.kg_to_lb(50), 110.23113109244001)

    def test_convert_weight(self):
        self.assertEqual(utils.convert_weight(50), "110.23 lbs")


if __name__ == "__main__":
    unittest.main()
