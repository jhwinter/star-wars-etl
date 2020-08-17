import unittest

from star_wars_etl.common import DB_NAME, open_db
from star_wars_etl.task_one import (
    get_film_title,
    get_random_characters_films,
    insert_characters,
    insert_films,
    insert_character_film,
    get_characters,
    get_character,
    get_films,
    get_film,
    get_character_join_film,
    get_film_join_character,
    add_characters_films,
    get_output,
    main,
)


class TestTaskOne(unittest.TestCase):
    def test_get_film_title(self):
        pass

    def test_get_random_characters_films(self):
        pass

    def test_insert_characters(self):
        pass

    def test_insert_films(self):
        pass

    def test_insert_character_film(self):
        pass

    def test_get_characters(self):
        pass

    def test_get_character(self):
        pass

    def test_get_films(self):
        pass

    def test_get_film(self):
        pass

    def test_get_character_join_film(self):
        pass

    def test_get_film_join_character(self):
        pass

    def test_add_characters_films(self):
        pass

    def test_get_output(self):
        pass

    def test_main(self):
        pass


if __name__ == "__main__":
    unittest.main()
