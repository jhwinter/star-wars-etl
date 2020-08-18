import unittest

import responses

from star_wars_etl import task_one, utils
from star_wars_etl.test import test_db_utils


class TestTaskOne(unittest.TestCase):
    @responses.activate
    def test_get_film_data(self):
        url = utils.generate_url("films")(1)
        mock_res = {"title": "test film", "url": url}
        responses.add(responses.GET, url, json=mock_res, status=200)

        resp = task_one.get_film_data(url)
        expected_result = (mock_res.get("title"), mock_res.get("url"))
        self.assertEqual(resp, expected_result)

    @responses.activate
    def test_get_characters_films(self):
        char_url = utils.generate_url("people")(1)
        film_url = utils.generate_url("films")
        mock_char_res = {
            "name": "test people",
            "url": char_url,
            "films": [
                film_url(1),
                film_url(2),
                film_url(3),
            ]
        }
        responses.add(responses.GET, char_url, json=mock_char_res, status=200)

        mock_film_resps = [
            {"title": "test film 1", "url": film_url(1)},
            {"title": "test film 2", "url": film_url(2)},
            {"title": "test film 3", "url": film_url(3)}
        ]
        responses.add(responses.GET, film_url(1),
                      json=mock_film_resps[0], status=200)
        responses.add(responses.GET, film_url(2),
                      json=mock_film_resps[1], status=200)
        responses.add(responses.GET, film_url(3),
                      json=mock_film_resps[2], status=200)

        resp = task_one.get_characters_films(1)
        expected_result = (
            mock_char_res.get("name"),
            mock_char_res.get("url"),
            [(mock_res.get("title"), mock_res.get("url"))
             for mock_res in mock_film_resps]
        )
        self.assertEqual(resp, expected_result)

    def test_add_characters_films(self):
        pass

    def test_get_output(self):
        pass

    def test_main(self):
        pass


if __name__ == "__main__":
    unittest.main()
