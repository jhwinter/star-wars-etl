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

from star_wars_etl import utils

CHARACTERS = "characters"
PLANETS = "planets"
SPECIES = "species"
STARSHIPS = "starships"
VEHICLES = "vehicles"


def get_film(api_film_id=1):
    """Retrieves data from the film endpoint"""
    return utils.get_data(utils.generate_url("films")(api_film_id))


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
    all cross-referencing material, and converts the
    height (cm) and mass (kg) to ft + in and weight (lb)
    for all characters"""
    resources = {CHARACTERS, PLANETS, SPECIES, STARSHIPS, VEHICLES}
    for resource in resources:
        for idx, endpoint in enumerate(film_data[resource]):
            film_data[resource][idx] = sanitize_cross_ref_mat_data(
                utils.get_data(endpoint), resource
            )
            if resource == CHARACTERS:
                std_height = utils.convert_height(
                    film_data[resource][idx]["height"])
                std_weight = utils.convert_weight(
                    film_data[resource][idx]["mass"])
                film_data[resource][idx]["height"] = std_height
                film_data[resource][idx]["weight"] = std_weight
                film_data[resource][idx].pop("mass", None)

    return film_data


def main():
    """entrypoint of program"""
    film = get_film()
    output = format_film_data(film.copy())
    json_output = utils.get_json(output)
    parent_dir = pathlib.Path(__file__).parent.parent
    with open(parent_dir.joinpath("task_two.json"), "w") as f:
        f.write(json_output)

    return json_output


if __name__ == "__main__":
    main()
