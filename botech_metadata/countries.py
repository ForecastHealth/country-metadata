from typing import NamedTuple, List
import csv


COUNTRY_FILEPATH = "botech_metadata/countries.csv"


class Country(NamedTuple):
    name: str
    alpha2: str
    alpha3: str
    numeric: str
    apolitical_name: str


def collect_country_data(fp: str) -> List[Country]:
    countries = []
    with open(fp, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            if row:  # Ensure the row is not empty
                country = Country(*row)
                countries.append(country)
    return countries
