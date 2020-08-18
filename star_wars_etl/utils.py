#!/usr/bin/env python3
import json

import requests

STAR_WARS_API = "https://swapi.dev/api"


# general
def remove_none(a_list):
    """Removes all None values from a list"""
    return [x for x in a_list if x is not None]


def get_json(data):
    """Converts data to JSON format"""
    return json.dumps(data, indent=4, ensure_ascii=False)


def generate_url(resource):
    def get_resource(resource_id):
        return f"{STAR_WARS_API}/{resource}/{resource_id}/"

    return get_resource


# requests
def is_valid_response(response):
    """Ensures that the response has data"""
    if response and response.status_code == 200:
        return response.json()


def get_data(endpoint):
    """Retrieves the data from the endpoint and checks it's validity"""
    return is_valid_response(requests.get(endpoint))


# conversions
# height
def cm_to_in(x):
    """Converts centimeters to inches"""
    return x * 0.3937008


def in_to_ft(x):
    """Converts inches to feet --rounded down"""
    return int(x // 12)


def convert_height(height):
    """Converts the height in centimeters to feet + inches as a string"""
    output = "{} ft {} in"
    try:
        height_in = cm_to_in(int(height))
        return output.format(
            in_to_ft(height_in),
            round(height_in % 12, 2)
        )
    except ValueError:
        return output.format(height)


# mass/weight
def kg_to_lb(x):
    """Converts kilograms to pounds"""
    return x * 2.2046226218488


def convert_weight(mass):
    """Converts the mass in kilograms to pounds as a string"""
    output = "{} lbs"
    try:
        return output.format(round(kg_to_lb(int(mass)), 2))
    except ValueError:
        return output.format(mass)
