#!/usr/bin/env python3
import json
import os

from dotenv import load_dotenv
import pymysql
import requests

load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME", "star_wars")

STAR_WARS_API = "https://swapi.dev/api"


# general
def remove_none(a_list):
    """Removes all None values from a list"""
    return [x for x in a_list if x is not None]


def get_json(data):
    """Converts data to JSON format"""
    return json.dumps(data, indent=4, ensure_ascii=False)


# requests
def is_valid_response(response):
    """Ensures that the response has data"""
    if response and response.status_code == 200:
        return response.json()


def get_endpoint_data(endpoint):
    """Retrieves the data from the endpoint and checks it's validity"""
    return is_valid_response(requests.get(endpoint))


# db
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
