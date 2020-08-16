import pymysql

from constants import DB_USER, DB_PASS, DB_NAME


def open_db(include_db=False):
    return pymysql.connect(
        host="localhost",
        user=DB_USER,
        password=DB_PASS,
        charset="utf8",
        database=DB_NAME if include_db else None,
        cursorclass=pymysql.cursors.DictCursor
    )
