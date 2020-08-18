import copy
import json
import pathlib
import unittest

import responses

from star_wars_etl import create_db, task_two, utils

RESOURCES = {
    task_two.CHARACTERS,
    task_two.PLANETS,
    task_two.SPECIES,
    task_two.STARSHIPS,
    task_two.VEHICLES,
}
mock_film_res = {
    "title": "A New Hope",
    "episode_id": 4,
    "opening_crawl": "It is a period of civil war.\r\nRebel spaceships, striking\r\nfrom a hidden base, have won\r\ntheir first victory against\r\nthe evil Galactic Empire.\r\n\r\nDuring the battle, Rebel\r\nspies managed to steal secret\r\nplans to the Empire's\r\nultimate weapon, the DEATH\r\nSTAR, an armored space\r\nstation with enough power\r\nto destroy an entire planet.\r\n\r\nPursued by the Empire's\r\nsinister agents, Princess\r\nLeia races home aboard her\r\nstarship, custodian of the\r\nstolen plans that can save her\r\npeople and restore\r\nfreedom to the galaxy....",
    "director": "George Lucas",
    "producer": "Gary Kurtz, Rick McCallum",
    "release_date": "1977-05-25",
    "characters": [
        "http://swapi.dev/api/people/1/",
    ],
    "planets": [
        "http://swapi.dev/api/planets/1/",
    ],
    "starships": [
        "http://swapi.dev/api/starships/2/",
    ],
    "vehicles": [
        "http://swapi.dev/api/vehicles/4/",
    ],
    "species": [
        "http://swapi.dev/api/species/1/",
    ],
    "created": "2014-12-10T14:23:31.880000Z",
    "edited": "2014-12-20T19:49:45.256000Z",
    "url": "http://swapi.dev/api/films/1/"
}
mock_char_res = {
    "name": "Luke Skywalker",
    "height": "172",
    "mass": "77",
    "hair_color": "blond",
    "skin_color": "fair",
    "eye_color": "blue",
    "birth_year": "19BBY",
    "gender": "male",
    "homeworld": "http://swapi.dev/api/planets/1/",
    "films": [
        "http://swapi.dev/api/films/1/",
        "http://swapi.dev/api/films/2/",
        "http://swapi.dev/api/films/3/",
        "http://swapi.dev/api/films/6/"
    ],
    "species": [],
    "vehicles": [
        "http://swapi.dev/api/vehicles/14/",
        "http://swapi.dev/api/vehicles/30/"
    ],
    "starships": [
        "http://swapi.dev/api/starships/12/",
        "http://swapi.dev/api/starships/22/"
    ],
    "created": "2014-12-09T13:50:51.644000Z",
    "edited": "2014-12-20T21:17:56.891000Z",
    "url": "http://swapi.dev/api/people/1/"
}
mock_planet_res = {
    "name": "Yavin IV",
    "rotation_period": "24",
    "orbital_period": "4818",
    "diameter": "10200",
    "climate": "temperate, tropical",
    "gravity": "1 standard",
    "terrain": "jungle, rainforests",
    "surface_water": "8",
    "population": "1000",
    "residents": [],
    "films": [
        "http://swapi.dev/api/films/1/"
    ],
    "created": "2014-12-10T11:37:19.144000Z",
    "edited": "2014-12-20T20:58:18.421000Z",
    "url": "http://swapi.dev/api/planets/3/"
}
mock_species_res = {
    "name": "Human",
    "classification": "mammal",
    "designation": "sentient",
    "average_height": "180",
    "skin_colors": "caucasian, black, asian, hispanic",
    "hair_colors": "blonde, brown, black, red",
    "eye_colors": "brown, blue, green, hazel, grey, amber",
    "average_lifespan": "120",
    "homeworld": "http://swapi.dev/api/planets/9/",
    "language": "Galactic Basic",
    "people": [
        "http://swapi.dev/api/people/66/",
        "http://swapi.dev/api/people/67/",
        "http://swapi.dev/api/people/68/",
        "http://swapi.dev/api/people/74/"
    ],
    "films": [
        "http://swapi.dev/api/films/1/",
        "http://swapi.dev/api/films/2/",
        "http://swapi.dev/api/films/3/",
        "http://swapi.dev/api/films/4/",
        "http://swapi.dev/api/films/5/",
        "http://swapi.dev/api/films/6/"
    ],
    "created": "2014-12-10T13:52:11.567000Z",
    "edited": "2014-12-20T21:36:42.136000Z",
    "url": "http://swapi.dev/api/species/1/"
}
mock_starship_res = {
    "name": "Death Star",
    "model": "DS-1 Orbital Battle Station",
    "manufacturer": "Imperial Department of Military Research, Sienar Fleet Systems",
    "cost_in_credits": "1000000000000",
    "length": "120000",
    "max_atmosphering_speed": "n/a",
    "crew": "342,953",
    "passengers": "843,342",
    "cargo_capacity": "1000000000000",
    "consumables": "3 years",
    "hyperdrive_rating": "4.0",
    "MGLT": "10",
    "starship_class": "Deep Space Mobile Battlestation",
    "pilots": [],
    "films": [
        "http://swapi.dev/api/films/1/"
    ],
    "created": "2014-12-10T16:36:50.509000Z",
    "edited": "2014-12-20T21:26:24.783000Z",
    "url": "http://swapi.dev/api/starships/9/"
}
mock_vehicles_res = {
    "name": "Sand Crawler",
    "model": "Digger Crawler",
    "manufacturer": "Corellia Mining Corporation",
    "cost_in_credits": "150000",
    "length": "36.8 ",
    "max_atmosphering_speed": "30",
    "crew": "46",
    "passengers": "30",
    "cargo_capacity": "50000",
    "consumables": "2 months",
    "vehicle_class": "wheeled",
    "pilots": [],
    "films": [
        "http://swapi.dev/api/films/1/",
        "http://swapi.dev/api/films/5/"
    ],
    "created": "2014-12-10T15:36:25.724000Z",
    "edited": "2014-12-20T21:30:21.661000Z",
    "url": "http://swapi.dev/api/vehicles/4/"
}
cross_ref_mats = {
    task_two.CHARACTERS: {"films", "homeworld", "starships", "species",
                          "vehicles"},
    task_two.PLANETS: {"films", "residents"},
    task_two.SPECIES: {"films", "homeworld", "people"},
    task_two.STARSHIPS: {"films", "pilots"},
    task_two.VEHICLES: {"films", "pilots"},
}
cross_ref_data = {
    task_two.CHARACTERS: mock_char_res,
    task_two.PLANETS: mock_planet_res,
    task_two.SPECIES: mock_species_res,
    task_two.STARSHIPS: mock_starship_res,
    task_two.VEHICLES: mock_vehicles_res,
}


class TestTaskTwo(unittest.TestCase):
    def test_get_film(self):
        url = utils.generate_url("films")(1)
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, url, json=mock_film_res, status=200)
            resp = task_two.get_film(1)
            rsps.reset()

        self.assertEqual(resp, mock_film_res)

    def test_sanitize_cross_ref_mat_data(self):
        for resource in RESOURCES:
            cross_ref_mat = task_two.sanitize_cross_ref_mat_data(
                copy.deepcopy(cross_ref_data[resource]),
                resource
            )
            for cross_ref_resource in cross_ref_mats[resource]:
                self.assertNotIn(cross_ref_resource, cross_ref_mat)

    def test_format_film_data(self):
        film_url = utils.generate_url("films")(1)
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, film_url,
                     json=mock_film_res, status=200)
            rsps.add(responses.GET, mock_film_res[task_two.CHARACTERS][0],
                     json=mock_char_res, status=200)
            rsps.add(responses.GET, mock_film_res[task_two.PLANETS][0],
                     json=mock_planet_res, status=200)
            rsps.add(responses.GET, mock_film_res[task_two.SPECIES][0],
                     json=mock_species_res, status=200)
            rsps.add(responses.GET, mock_film_res[task_two.STARSHIPS][0],
                     json=mock_starship_res, status=200)
            rsps.add(responses.GET, mock_film_res[task_two.VEHICLES][0],
                     json=mock_vehicles_res, status=200)
            resp = task_two.format_film_data(copy.deepcopy(mock_film_res))
            rsps.reset()

        self.assertIsInstance(resp, dict)
        self.assertIn("weight", resp[task_two.CHARACTERS][0])
        self.assertNotIn("mass", resp[task_two.CHARACTERS][0])
        self.assertEqual(
            resp[task_two.CHARACTERS][0]["height"],
            utils.convert_height(mock_char_res["height"])
        )
        self.assertEqual(
            resp[task_two.CHARACTERS][0]["weight"],
            utils.convert_weight(mock_char_res["mass"])
        )

    def test_main(self):
        film_url = utils.generate_url("films")(1)
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, film_url,
                     json=mock_film_res, status=200)
            rsps.add(responses.GET, mock_film_res[task_two.CHARACTERS][0],
                     json=mock_char_res, status=200)
            rsps.add(responses.GET, mock_film_res[task_two.PLANETS][0],
                     json=mock_planet_res, status=200)
            rsps.add(responses.GET, mock_film_res[task_two.SPECIES][0],
                     json=mock_species_res, status=200)
            rsps.add(responses.GET, mock_film_res[task_two.STARSHIPS][0],
                     json=mock_starship_res, status=200)
            rsps.add(responses.GET, mock_film_res[task_two.VEHICLES][0],
                     json=mock_vehicles_res, status=200)
            json_output = task_two.main()
            rsps.reset()

        self.assertIsInstance(json_output, str)
        dict_output = json.loads(json_output)
        self.assertIsInstance(dict_output, dict)
        self.assertIn("weight", dict_output[task_two.CHARACTERS][0])
        self.assertNotIn("mass", dict_output[task_two.CHARACTERS][0])
        self.assertEqual(
            dict_output[task_two.CHARACTERS][0]["height"],
            utils.convert_height(mock_char_res["height"])
        )
        self.assertEqual(
            dict_output[task_two.CHARACTERS][0]["weight"],
            utils.convert_weight(mock_char_res["mass"])
        )
        parent_dir = pathlib.Path(__file__).parent.parent.parent
        filepath = parent_dir.joinpath("task_two.json")
        self.assertTrue(filepath.is_file())


if __name__ == "__main__":
    create_db.main()
    unittest.main()
