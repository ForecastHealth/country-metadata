import unittest
from botech_metadata import (
    get_country,
    get_tag,
    get_countries_by_tags,
    Country,
    Tag,
)


class TestAPI(unittest.TestCase):

    def test_get_country(self):
        country = get_country("AFG")
        self.assertIsNotNone(country)
        self.assertEqual(country.name, "Afghanistan")

        country = get_country("Australia")
        self.assertIsNotNone(country)
        self.assertEqual(country.alpha2, "AU")

        country = get_country("Invalid")
        self.assertIsNone(country)

    def test_get_tag(self):
        tag_value = get_tag("AU", "appendix_3")
        self.assertEqual(tag_value, 0)

        tag_value = get_tag("AUS", "wb_income")
        self.assertEqual(tag_value, "High income")

        tag_value = get_tag(36, "wb_region")
        self.assertEqual(tag_value, "East Asia & Pacific")

        tag_value = get_tag("Australia", "who_region")
        self.assertEqual(tag_value, "Australasia")

        tag_value = get_tag("AU", "tag1")
        self.assertIsNone(tag_value)

        tag_value = get_tag("C1", "invalid_tag")
        self.assertIsNone(tag_value)

    def test_countries_by_tags(self):
        dictionary_of_countries = get_countries_by_tags("appendix_3", "wb_income")
        print(dictionary_of_countries.keys())


if __name__ == '__main__':
    unittest.main()

