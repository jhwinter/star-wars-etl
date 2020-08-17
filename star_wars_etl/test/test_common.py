import json

import unittest
from unittest.mock import Mock

from requests.models import Response

from star_wars_etl.common import (
    remove_none,
    get_json,
    is_valid_response,
    get_endpoint_data,
    open_db,
)


class TestCommon(unittest.TestCase):
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
        self.assertEqual(remove_none(a_list), expected_result)

    def test_get_json(self):
        a_dict = {
            "blah": "blue",
            "test": "testing",
            "number": 100
        }
        expected_result = json.dumps(a_dict, indent=4, ensure_ascii=False)
        self.assertEqual(get_json(a_dict), expected_result)

    def test_is_valid_response(self):
        the_response = Mock(spec=Response)
        the_response.json.return_value = {"test": "tester"}
        the_response.status_code = 200
        self.assertEqual(
            is_valid_response(the_response),
            the_response.json.return_value
        )

    def test_get_endpoint_data(self):
        pass

    def test_open_db(self):
        self.assertEqual(open_db().open, True)


if __name__ == "__main__":
    unittest.main()
