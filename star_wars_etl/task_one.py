#!/usr/bin/env python3
"""Task 1
The Star Wars API lists 87 main characters in the Star Wars saga.
For the first task we would like you to use a random number generator
that picks a number between 1-87.
Using these random numbers you will be pulling 15 characters from the
API using Python.
We would like you to:
    1. GET 15 random characters and the names of the films
    they have been in using Python.
    2. Insert into MySQL - Please include SQL database schema(s)
    for any table(s) created in your Github repo
    3. Write a script called task_one.py that when called will output
    something like this to the console.
"""
import contextlib
import random

from star_wars_etl import create_db, db_utils, utils


def get_film_data(film_endpoint):
    """

    :param film_endpoint:
    :return:
    """
    res = utils.get_data(film_endpoint)
    if not res:
        return
    return res.get("title"), res.get("url")


def get_characters_films(character_resource_id):
    """

    :return:
    """
    endpoint = utils.generate_url("people")(character_resource_id)
    res = utils.get_data(endpoint)
    if not res:
        return

    film_endpoints = res.get("films")
    films = []
    if film_endpoints:
        films = [get_film_data(film_endpoint)
                 for film_endpoint in film_endpoints]
    return res.get("name"), res.get("url"), utils.remove_none(films)


def add_characters_films(connection, characters_films, characters, films):
    """

    :param connection:
    :param characters_films:
    :param characters:
    :param films:
    :return:
    """
    try:
        with contextlib.closing(connection.cursor()) as cursor:
            db_utils.insert_characters(cursor, characters)
            db_utils.insert_films(cursor, films)
            connection.commit()
        with contextlib.closing(connection.cursor()) as cursor:
            for character_film in characters_films:
                character_id = db_utils.get_character(
                    cursor, character_film[0]).get("id")
                character_film_ids = [
                    (character_id,
                     db_utils.get_film(cursor, film[0]).get("id"))
                    for film in character_film[2]
                ]
                if character_film_ids:
                    db_utils.insert_character_film(cursor, character_film_ids)
            connection.commit()
        return True
    except:
        connection.rollback()
        raise


def get_output(connection):
    """

    :param connection:
    :type connection:
    :return:
    :rtype:
    """
    with contextlib.closing(connection.cursor()) as cursor:
        db_films = db_utils.get_films(cursor)
        output = []
        for film in db_films:
            film_characters = db_utils.get_film_join_character(
                cursor, film.get("id"))
            output.append(
                {
                    "film": film.get("title"),
                    "character": [character.get("name")
                                  for character in film_characters]
                }
            )

    return output


def main():
    """entrypoint to the program"""
    # building list of unique character-film combinations
    characters_films = utils.remove_none(
        [get_characters_films(random.randint(1, 87)) for _ in range(1, 15)]
    )
    # building list of unique characters
    characters = utils.remove_none(list(set(
        [character_film[:2] for character_film in characters_films]
    )))
    # building list of unique films
    films = utils.remove_none(list(set(
        [film for character_film in characters_films
         for film in character_film[2]]
    )))

    with contextlib.closing(db_utils.open_db(True)) as connection:
        # inserting data into database
        add_characters_films(connection, characters_films, characters, films)
        # retrieving the output
        output = get_output(connection)

    json_output = utils.get_json(output)
    print(json_output)
    return json_output


if __name__ == "__main__":
    create_db.main()
    main()
