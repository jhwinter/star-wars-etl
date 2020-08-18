import os

import dotenv
import pymysql

dotenv.load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME", "star_wars")


def open_db(include_db=False):
    """Opens a db connection"""
    return pymysql.connect(
        host="localhost",
        user=DB_USER,
        password=DB_PASS,
        charset="utf8",
        database=DB_NAME if include_db else None,
        cursorclass=pymysql.cursors.DictCursor
    )


# create
def insert_characters(cursor, characters):
    """Inserts characters into the database"""
    sql = "INSERT IGNORE INTO `character` (name, endpoint) VALUES (%s, %s)"
    return cursor.executemany(sql, characters)


def insert_films(cursor, films):
    """Inserts films into the database"""
    sql = "INSERT IGNORE INTO `film` (title, endpoint) VALUES (%s, %s)"
    return cursor.executemany(sql, films)


def insert_character_film(cursor, character_film_ids):
    """Inserts character_id and film_id into the join table"""
    sql = '''INSERT IGNORE INTO `character_film` (character_id, film_id)
    VALUES (%s, %s)'''
    return cursor.executemany(sql, character_film_ids)


# read
def get_characters(cursor):
    """Retrieves all characters from the database"""
    sql = "SELECT id, name, endpoint FROM `character`"
    cursor.execute(sql)
    return cursor.fetchall()


def get_character(cursor, name):
    """Retrieves a character from the database with a given name"""
    sql = "SELECT id, name, endpoint FROM `character` WHERE name = %s"
    cursor.execute(sql, (name,))
    return cursor.fetchone()


def get_films(cursor):
    """Retrieves all films from the database"""
    sql = "SELECT id, title, endpoint FROM `film`"
    cursor.execute(sql)
    return cursor.fetchall()


def get_film(cursor, title):
    """Retrieves a film from the database with a given title"""
    sql = "SELECT id, title, endpoint FROM `film` WHERE title = %s"
    cursor.execute(sql, (title,))
    return cursor.fetchone()


def get_character_join_film(cursor, character_id):
    """Retrieves character and film information given a character id"""
    sql = '''SELECT character.id, character.name, character.endpoint, 
    film.id, film.title, film.endpoint 
    FROM `character_film` 
    INNER JOIN `character` ON character_film.character_id = character.id
    INNER JOIN `film` ON character_film.film_id = film.id
    WHERE character.id = %s
    '''
    cursor.execute(sql, (character_id,))
    return cursor.fetchall()


def get_film_join_character(cursor, film_id):
    """Retrieves character and film information given a film id"""
    sql = '''SELECT film.id, film.title, film.endpoint, 
    character.id, character.name, character.endpoint 
    FROM `character_film`
    INNER JOIN `character` ON character_film.character_id = character.id
    INNER JOIN `film` ON character_film.film_id = film.id
    WHERE film.id = %s
    '''
    cursor.execute(sql, (film_id,))
    return cursor.fetchall()
