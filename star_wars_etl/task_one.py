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

from .common import (
    DB_NAME,
    STAR_WARS_API,
    get_endpoint_data,
    get_json,
    open_db,
    remove_none,
)
from .create_db import main as create_db__main


def get_film_title(film_endpoint):
    """

    :param film_endpoint:
    :return:
    """
    res = get_endpoint_data(film_endpoint)
    if not res:
        return
    return res.get("title"), res.get("url")


def get_random_characters_films():
    """

    :return:
    """
    endpoint = f"{STAR_WARS_API}/people/{random.randint(1, 87)}"
    res = get_endpoint_data(endpoint)
    if not res:
        return

    film_endpoints = res.get("films")
    films = []
    if film_endpoints:
        films = [get_film_title(film_endpoint)
                 for film_endpoint in film_endpoints]
    return res.get("name"), res.get("url"), remove_none(films)


def insert_characters(cursor, characters):
    """

    :param cursor:
    :param characters:
    :return:
    """
    sql = "INSERT IGNORE INTO `character` (name, endpoint) VALUES (%s, %s)"
    return cursor.executemany(sql, characters)


def insert_films(cursor, films):
    """

    :param cursor:
    :param films:
    :return:
    """
    sql = "INSERT IGNORE INTO `film` (title, endpoint) VALUES (%s, %s)"
    return cursor.executemany(sql, films)


def insert_character_film(cursor, character_film_ids):
    """

    :param cursor:
    :param character_film_ids:
    :return:
    """
    sql = '''INSERT IGNORE INTO `character_film` (character_id, film_id)
    VALUES (%s, %s)'''
    return cursor.executemany(sql, character_film_ids)


def get_characters(cursor):
    """

    :param cursor:
    :return:
    """
    sql = "SELECT id, name, endpoint FROM `character`"
    cursor.execute(sql)
    return cursor.fetchall()


def get_character(cursor, name):
    """

    :param cursor:
    :param name:
    :return:
    """
    sql = "SELECT id, name, endpoint FROM `character` WHERE name = %s"
    cursor.execute(sql, (name,))
    return cursor.fetchone()


def get_films(cursor):
    """

    :param cursor:
    :return:
    """
    sql = "SELECT id, title, endpoint FROM `film`"
    cursor.execute(sql)
    return cursor.fetchall()


def get_film(cursor, title):
    """

    :param cursor:
    :param title:
    :return:
    """
    sql = "SELECT id, title, endpoint FROM `film` WHERE title = %s"
    cursor.execute(sql, (title,))
    return cursor.fetchone()


def get_character_join_film(cursor, character_id):
    """

    :param cursor:
    :param character_id:
    :return:
    """
    sql = '''SELECT character.name, character.endpoint, 
    film.title, film.endpoint 
    FROM `character_film` 
    INNER JOIN `character` ON character_film.character_id = character.id
    INNER JOIN `film` ON character_film.film_id = film.id
    WHERE character.id = %s
    '''
    cursor.execute(sql, (character_id,))
    return cursor.fetchall()


def get_film_join_character(cursor, film_id):
    """

    :param cursor:
    :param film_id:
    :return:
    """
    sql = '''SELECT film.title, film.endpoint, 
    character.name, character.endpoint 
    FROM `character_film`
    INNER JOIN `character` ON character_film.character_id = character.id
    INNER JOIN `film` ON character_film.film_id = film.id
    WHERE film.id = %s
    '''
    cursor.execute(sql, (film_id,))
    return cursor.fetchall()


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
            insert_characters(cursor, characters)
            insert_films(cursor, films)
            connection.commit()
        with contextlib.closing(connection.cursor()) as cursor:
            for character_film in characters_films:
                character_id = get_character(cursor,
                                             character_film[0]).get("id")
                character_film_ids = [
                    (character_id, get_film(cursor, film[0]).get("id"))
                    for film in character_film[2]
                ]
                if character_film_ids:
                    insert_character_film(cursor, character_film_ids)
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
        db_films = get_films(cursor)
        output = []
        for film in db_films:
            film_characters = get_film_join_character(cursor, film.get("id"))
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
    characters_films = remove_none(
        [get_random_characters_films() for _ in range(1, 15)]
    )
    # building list of unique characters
    characters = remove_none(list(set(
        [character_film[:2] for character_film in characters_films]
    )))
    # building list of unique films
    films = remove_none(list(set(
        [film for character_film in characters_films
         for film in character_film[2]]
    )))

    with contextlib.closing(open_db(DB_NAME)) as connection:
        # inserting data into database
        add_characters_films(connection, characters_films, characters, films)
        # retrieving the output
        output = get_output(connection)

    json_output = get_json(output)
    print(json_output)
    return json_output


if __name__ == "__main__":
    create_db__main()
    main()
