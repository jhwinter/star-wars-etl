import contextlib
import json
import re
import unittest

import responses

from star_wars_etl import create_db, db_utils, task_one, utils


class TestTaskOne(unittest.TestCase):
    def test_get_film_data(self):
        url = utils.generate_url("films")(1)
        mock_res = {"title": "test film", "url": url}
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, url, json=mock_res, status=200)
            resp = task_one.get_film_data(url)
            rsps.reset()

        expected_result = (mock_res.get("title"), mock_res.get("url"))
        self.assertEqual(resp, expected_result)

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
        mock_film_resps = [
            {"title": "test film 1", "url": film_url(1)},
            {"title": "test film 2", "url": film_url(2)},
            {"title": "test film 3", "url": film_url(3)}
        ]
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, char_url,
                     json=mock_char_res, status=200)
            rsps.add(responses.GET, film_url(1),
                     json=mock_film_resps[0], status=200)
            rsps.add(responses.GET, film_url(2),
                     json=mock_film_resps[1], status=200)
            rsps.add(responses.GET, film_url(3),
                     json=mock_film_resps[2], status=200)
            resp = task_one.get_characters_films(1)
            rsps.reset()

        expected_result = (
            mock_char_res.get("name"),
            mock_char_res.get("url"),
            [(mock_res.get("title"), mock_res.get("url"))
             for mock_res in mock_film_resps]
        )
        self.assertEqual(resp, expected_result)

    def test_add_characters_films(self):
        char_url = utils.generate_url("people")
        char_insert_data = [
            ("test character 1", char_url(1)),
            ("test character 2", char_url(2)),
            ("test character 3", char_url(3))
        ]
        film_url = utils.generate_url("films")
        film_insert_data = [
            ("test film 1", film_url(1)),
            ("test film 2", film_url(2)),
            ("test film 3", film_url(3))
        ]
        characters_films_insert_data = [
            (character[0], character[1], film_insert_data)
            for character in char_insert_data
        ]
        with contextlib.closing(db_utils.open_db(True)) as conn:
            task_one.add_characters_films(
                conn,
                characters_films_insert_data,
                char_insert_data,
                film_insert_data
            )
            with contextlib.closing(conn.cursor()) as cursor:
                for row in char_insert_data:
                    character = db_utils.get_character(cursor, row[0])
                    self.assertEqual(character.get("name"), row[0])
                    self.assertEqual(character.get("endpoint"), row[1])

                for row in film_insert_data:
                    film = db_utils.get_film(cursor, row[0])
                    self.assertEqual(film.get("title"), row[0])
                    self.assertEqual(film.get("endpoint"), row[1])

    def test_get_output(self):
        self.test_add_characters_films()
        with contextlib.closing(db_utils.open_db(True)) as conn:
            output = task_one.get_output(conn)

        self.assertIsInstance(output, list)
        for row in output:
            self.assertIsInstance(row, dict)
            self.assertIn("film", row)
            self.assertIn("character", row)
            self.assertIsInstance(row["film"], str)
            self.assertIsInstance(row["character"], list)

    def test_main(self):
        char_url = utils.generate_url("people")
        film_url = utils.generate_url("films")
        mock_char_res = {
            "name": "test people",
            "url": char_url(100),
            "films": [
                film_url(100),
                film_url(200),
                film_url(300),
            ]
        }
        mock_film_res = {"title": "test film", "url": film_url(100)}
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, re.compile(char_url("[0-9]*")),
                     json=mock_char_res, status=200)
            rsps.add(responses.GET, re.compile(film_url("[0-9]*")),
                     json=mock_film_res, status=200)
            json_output = task_one.main()
            rsps.reset()

        self.assertIsInstance(json_output, str)
        dict_output = json.loads(json_output)
        self.assertIsInstance(dict_output, list)
        for row in dict_output:
            self.assertIsInstance(row, dict)
            self.assertIn("film", row)
            self.assertIn("character", row)
            self.assertIsInstance(row["film"], str)
            self.assertIsInstance(row["character"], list)


if __name__ == "__main__":
    create_db.main()
    unittest.main()
