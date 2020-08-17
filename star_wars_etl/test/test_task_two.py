import unittest

from star_wars_etl.task_two import (
    cm_to_in,
    in_to_ft,
    convert_height,
    kg_to_lb,
    convert_weight,
    get_film,
    sanitize_cross_ref_mat_data,
    format_film_data,
    main,
)


class TestTaskTwo(unittest.TestCase):
    def test_cm_to_in(self):
        self.assertEqual(cm_to_in(50), 19.68504)

    def test_in_to_ft(self):
        self.assertEqual(in_to_ft(50), 4)

    def test_convert_height(self):
        self.assertEqual(convert_height(170), "5 ft 6.93 in")

    def test_kg_to_lb(self):
        self.assertEqual(kg_to_lb(50), 110.23113109244001)

    def test_convert_weight(self):
        self.assertEqual(convert_weight(50), "110.23 lbs")

    def test_get_film(self):
        pass

    def test_sanitize_cross_ref_mat_data(self):
        pass

    def test_format_film_data(self):
        pass

    def test_main(self):
        pass


if __name__ == "__main__":
    unittest.main()
