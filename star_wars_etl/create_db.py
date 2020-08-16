#!/usr/bin/env python3
import contextlib

from common import (
    DB_NAME,
    open_db,
)


def drop_database(cursor):
    """Drop database if already exists."""
    return cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")


def create_database(cursor):
    """Create database"""
    return cursor.execute(f"CREATE DATABASE {DB_NAME}")


def create_tables(cursor):
    """Create tables for character, film, and character_film"""
    # create character table
    create_character = '''CREATE TABLE `character` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `name` VARCHAR(128) NOT NULL,
        `endpoint` VARCHAR(128) NOT NULL,
        PRIMARY KEY (`id`),
        UNIQUE (`name`),
        UNIQUE (`endpoint`)
    )'''
    cursor.execute(create_character)

    # create film table
    create_film = '''CREATE TABLE `film` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `title` VARCHAR(128) NOT NULL,
        `endpoint` VARCHAR(128) NOT NULL,
        PRIMARY KEY (`id`),
        UNIQUE (`title`),
        UNIQUE (`endpoint`)
    )'''
    cursor.execute(create_film)

    # create character_film table
    create_character_film = '''CREATE TABLE `character_film` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `character_id` INT NOT NULL,
        `film_id` INT NOT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`character_id`) REFERENCES `character` (`id`),
        FOREIGN KEY (`film_id`) REFERENCES `film` (`id`),
        CONSTRAINT `uc_character_film` UNIQUE (`character_id`, `film_id`)
    )'''
    cursor.execute(create_character_film)
    return True


def main():
    """entrypoint of program"""
    with contextlib.closing(open_db()) as conn:
        with contextlib.closing(conn.cursor()) as cursor:
            drop_database(cursor)

            create_database(cursor)
            conn.select_db(DB_NAME)

            create_tables(cursor)

    return True


if __name__ == "__main__":
    main()
