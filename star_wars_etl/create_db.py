#!/usr/bin/env python3
import contextlib

from star_wars_etl import db_utils


def drop_database(conn):
    """Drop database if already exists."""
    with contextlib.closing(conn.cursor()) as cursor:
        cursor.execute(f"DROP DATABASE IF EXISTS {db_utils.DB_NAME}")
    return conn.commit()


def create_database(conn):
    """Create database"""
    with contextlib.closing(conn.cursor()) as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_utils.DB_NAME}")
    return conn.commit()


def create_tables(conn):
    """Create tables for character, film, and character_film"""
    with contextlib.closing(conn.cursor()) as cursor:
        # create character table
        create_character = '''CREATE TABLE IF NOT EXISTS `character` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `name` VARCHAR(128) NOT NULL,
            `endpoint` VARCHAR(128) NOT NULL,
            PRIMARY KEY (`id`),
            UNIQUE (`name`),
            UNIQUE (`endpoint`)
        )'''
        cursor.execute(create_character)

        # create film table
        create_film = '''CREATE TABLE IF NOT EXISTS `film` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `title` VARCHAR(128) NOT NULL,
            `endpoint` VARCHAR(128) NOT NULL,
            PRIMARY KEY (`id`),
            UNIQUE (`title`),
            UNIQUE (`endpoint`)
        )'''
        cursor.execute(create_film)

        # create character_film table
        create_character_film = '''CREATE TABLE IF NOT EXISTS`character_film` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `character_id` INT NOT NULL,
            `film_id` INT NOT NULL,
            PRIMARY KEY (`id`),
            FOREIGN KEY (`character_id`) REFERENCES `character` (`id`),
            FOREIGN KEY (`film_id`) REFERENCES `film` (`id`),
            CONSTRAINT `uc_character_film` UNIQUE (`character_id`, `film_id`)
        )'''
        cursor.execute(create_character_film)
    return conn.commit()


def main():
    """entrypoint of program"""
    with contextlib.closing(db_utils.open_db()) as conn:
        drop_database(conn)

        create_database(conn)
        conn.select_db(db_utils.DB_NAME)

        create_tables(conn)

    return True


if __name__ == "__main__":
    main()
