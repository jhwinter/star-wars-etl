import contextlib
import unittest

from star_wars_etl import db_utils, create_db


class TestCreateDB(unittest.TestCase):
    def helper__database_exists(self, conn, expected_result):
        sql = f"SHOW DATABASES LIKE '{db_utils.DB_NAME}'"
        with contextlib.closing(conn.cursor()) as cursor:
            results = cursor.execute(sql)
            self.assertEqual(results, expected_result)

    def helper__tables_created(self, conn, expected_result):
        tables = {"character", "film", "character_film"}
        for table in tables:
            sql = f"SHOW TABLES LIKE '{table}'"
            with contextlib.closing(conn.cursor()) as cursor:
                results = cursor.execute(sql)
                self.assertEqual(results, expected_result)

    def helper__database_tables_created(self, conn, expected_result):
        self.helper__database_exists(conn, expected_result)
        conn.select_db(db_utils.DB_NAME)
        self.helper__tables_created(conn, expected_result)

    def test_drop_database(self):
        with contextlib.closing(db_utils.open_db()) as conn:
            create_db.create_database(conn)
            create_db.drop_database(conn)
            self.helper__database_exists(conn, 0)

    def test_create_database(self):
        with contextlib.closing(db_utils.open_db()) as conn:
            create_db.create_database(conn)
            self.helper__database_exists(conn, 1)

    def test_create_tables(self):
        with contextlib.closing(db_utils.open_db()) as conn:
            create_db.create_database(conn)
            conn.select_db(db_utils.DB_NAME)
            create_db.create_tables(conn)
            self.helper__tables_created(conn, 1)

    def test_main(self):
        create_db.main()
        with contextlib.closing(db_utils.open_db()) as conn:
            self.helper__database_tables_created(conn, 1)


if __name__ == "__main__":
    unittest.main()
