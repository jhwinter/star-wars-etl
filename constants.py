#!/usr/bin/env python3
import os

from dotenv import load_dotenv


load_dotenv()

STAR_WARS_API = "https://swapi.dev/api"
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME", "star_wars")
