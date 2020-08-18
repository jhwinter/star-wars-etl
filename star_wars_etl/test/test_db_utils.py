import contextlib
import unittest

from star_wars_etl import create_db, db_utils, utils


class TestDBUtils(unittest.TestCase):
    @staticmethod
    def helper__insert_characters(cursor):
        url = utils.generate_url("people")
        insert_data = [
            ("test 1", url(1)),
            ("test 2", url(2)),
            ("test 3", url(3))
        ]
        db_utils.insert_characters(cursor, insert_data)
        return insert_data

    @staticmethod
    def helper__insert_films(cursor):
        url = utils.generate_url("people")
        insert_data = [
            ("test 1", url(1)),
            ("test 2", url(2)),
            ("test 3", url(3))
        ]
        db_utils.insert_films(cursor, insert_data)
        return insert_data

    def test_open_db(self):
        self.assertEqual(db_utils.open_db().open, True)

    def test_insert_characters(self):
        with contextlib.closing(db_utils.open_db(True).cursor()) as cursor:
            insert_data = TestDBUtils.helper__insert_characters(cursor)
            characters = db_utils.get_characters(cursor)
            for row, character in zip(insert_data, characters):
                self.assertIn(row[0], character.values())
                self.assertIn(row[1], character.values())

    def test_insert_films(self):
        with contextlib.closing(db_utils.open_db(True).cursor()) as cursor:
            insert_data = TestDBUtils.helper__insert_characters(cursor)
            films = db_utils.get_films(cursor)
            for row, film in zip(insert_data, films):
                self.assertIn(row[0], film.values())
                self.assertIn(row[1], film.values())

    def test_insert_character_film(self):
        with contextlib.closing(db_utils.open_db(True).cursor()) as cursor:
            insert_data = [
                (1, 10),
                (2, 20),
                (1, 30)
            ]
            db_utils.insert_character_film(cursor, insert_data)
            char_films = db_utils.get_character_join_film(
                cursor, insert_data[0][0])
            for row, char_film in zip(insert_data, char_films):
                if row[0] == 1:
                    self.assertIn(row[0], char_film.values())
                    self.assertIn(row[1], char_film.values())
                else:
                    self.assertNotIn(row[0], char_film.values())
                    self.assertNotIn(row[1], char_film.values())

    def test_get_characters(self):
        with contextlib.closing(db_utils.open_db(True).cursor()) as cursor:
            insert_data = TestDBUtils.helper__insert_characters(cursor)
            characters = db_utils.get_characters(cursor)
            for row, character in zip(insert_data, characters):
                self.assertIn(row[0], character.values())
                self.assertIn(row[1], character.values())

    def test_get_character(self):
        with contextlib.closing(db_utils.open_db(True).cursor()) as cursor:
            insert_data = TestDBUtils.helper__insert_characters(cursor)
            character = db_utils.get_character(cursor, insert_data[0][0])
            self.assertIn(insert_data[0][0], character.values())
            self.assertIn(insert_data[0][1], character.values())

    def test_get_films(self):
        with contextlib.closing(db_utils.open_db(True).cursor()) as cursor:
            insert_data = TestDBUtils.helper__insert_characters(cursor)
            films = db_utils.get_films(cursor)
            for row, film in zip(insert_data, films):
                self.assertIn(row[0], film.values())
                self.assertIn(row[1], film.values())

    def test_get_film(self):
        with contextlib.closing(db_utils.open_db(True).cursor()) as cursor:
            insert_data = TestDBUtils.helper__insert_characters(cursor)
            film = db_utils.get_character(cursor, insert_data[0][0])
            self.assertIn(insert_data[0][0], film.values())
            self.assertIn(insert_data[0][1], film.values())

    def test_get_character_join_film(self):
        self.test_insert_character_film()

    def test_get_film_join_character(self):
        with contextlib.closing(db_utils.open_db(True).cursor()) as cursor:
            insert_data = [
                (1, 10),
                (2, 20),
                (3, 10)
            ]
            db_utils.insert_character_film(cursor, insert_data)
            film_chars = db_utils.get_film_join_character(
                cursor, insert_data[0][1])
            for row, film_char in zip(insert_data, film_chars):
                if row[1] == 10:
                    self.assertIn(row[0], film_char.values())
                    self.assertIn(row[1], film_char.values())
                else:
                    self.assertNotIn(row[0], film_char.values())
                    self.assertNotIn(row[1], film_char.values())


if __name__ == "__main__":
    create_db.main()
    unittest.main()
