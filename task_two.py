#!/usr/bin/env python3
"""Task 2
Now we would like you to pull data from the films endpoint.
We would like you to do the following:
    1. Pull data for the movie A New Hope
    2. Replace the data for each of the endpoints listed in the
    JSON object you receive from the API request (e.g. - In the example
    above you would take all the character endpoints and pull the data
    from each of those endpoints then insert the data into the
    JSON object, etc.)
        a. A New Hope has character, planet, starship, vehicle, and
        species data you will need to retrieve and replace.
    3. We also ask that you convert the metric heights and weights of
    each character to standard units.
    4. You will also need to remove all cross referencing material
    from the data you replace
    (e.g. - When you pull Luke Skywalker you would want to remove
    cross-referencing urls from Luke’s JSON object (like films,
    species, vehicles, and spaceships.)
    5. Lastly, you will take the dictionary you created and write it
    out to a JSON file locally named task_two.json.
"""
import contextlib
import json
import random

import requests

from constants import STAR_WARS_API


def get_film(api_film_id=1):
    return requests.get(f"{STAR_WARS_API}/films/{api_film_id}").json()


def get_endpoint_data(endpoint):
    return requests.get(endpoint).json()


def format_film_data(film_data):
    endpoint_names = (
        "characters", "planets", "species", "starships", "vehicles"
    )
    for end_name in endpoint_names:
        for idx, endpoint in enumerate(film_data[end_name]):
            film_data[end_name][idx] = get_endpoint_data(endpoint)

    return film_data


def main():
    """entrypoint of program"""
    film = get_film()
    output = format_film_data(film.copy())
    print(json.dumps(output, indent=4))


if __name__ == "__main__":
    main()
