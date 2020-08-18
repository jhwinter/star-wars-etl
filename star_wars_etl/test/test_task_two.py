import unittest

import responses

from star_wars_etl import create_db, task_two, utils


class TestTaskTwo(unittest.TestCase):
    def test_get_film(self):
        url = utils.generate_url("films")(1)
        mock_res = {"title": "test film", "url": url}
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, url, json=mock_res, status=200)
            resp = task_two.get_film(url)

        self.assertEqual(resp, mock_res)

    def test_sanitize_cross_ref_mat_data(self):
        pass

    def test_format_film_data(self):
        pass

    def test_main(self):
        pass


if __name__ == "__main__":
    create_db.main()
    unittest.main()
