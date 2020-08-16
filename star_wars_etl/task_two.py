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
import pathlib

from common import (
    STAR_WARS_API,
    get_endpoint_data,
    get_json,
)

CHARACTERS = "characters"
PLANETS = "planets"
SPECIES = "species"
STARSHIPS = "starships"
VEHICLES = "vehicles"


def cm_to_in(x):
    """Converts centimeters to inches"""
    return x * 0.39370


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
            round(height_in % 12, 4)
        )
    except ValueError:
        return output.format(height)


def kg_to_lb(x):
    """Converts kilograms to pounds"""
    return x * 2.2046226218488


def convert_weight(mass):
    """Converts the mass in kilograms to pounds as a string"""
    output = "{} lbs"
    try:
        return output.format(round(kg_to_lb(int(mass)), 4))
    except ValueError:
        return output.format(mass)


def get_film(api_film_id=1):
    """Retrieves data from the film endpoint"""
    return get_endpoint_data(f"{STAR_WARS_API}/films/{api_film_id}")


def sanitize_cross_ref_mat_data(data, endpoint_name):
    """Removes cross-referencing material from characters, planets,
    species, starships, and vehicles"""
    cross_ref_mats = {
        CHARACTERS: {"films", "homeworld", "starships", "species", "vehicles"},
        PLANETS: {"films", "residents"},
        SPECIES: {"films", "homeworld", "people"},
        STARSHIPS: {"films", "pilots"},
        VEHICLES: {"films", "pilots"},
    }
    for mat in cross_ref_mats[endpoint_name]:
        data.pop(mat, None)

    return data


def format_film_data(film_data):
    """Retrieves the data from the reference endpoints, removes
    all cross-referencing material, and
    converts the height (cm) and mass (kg) to ft + in and weight (lb)
    for all characters

    :param film_data:
    :type film_data:
    :return:
    :rtype:
    """
    keys = (CHARACTERS, PLANETS, SPECIES, STARSHIPS, VEHICLES)
    for key in keys:
        for idx, endpoint in enumerate(film_data[key]):
            film_data[key][idx] = sanitize_cross_ref_mat_data(
                get_endpoint_data(endpoint), key
            )
            if key == CHARACTERS:
                std_height = convert_height(film_data[key][idx]["height"])
                std_weight = convert_weight(film_data[key][idx]["mass"])
                film_data[key][idx]["height"] = std_height
                film_data[key][idx]["weight"] = std_weight

    return film_data


def main():
    """entrypoint of program"""
    film = get_film()
    output = format_film_data(film.copy())
    json_output = get_json(output)
    parent_dir = pathlib.Path(__file__).parent
    with open(parent_dir.joinpath("task_two.json"), "w") as f:
        f.write(json_output)

    return json_output


if __name__ == "__main__":
    main()
