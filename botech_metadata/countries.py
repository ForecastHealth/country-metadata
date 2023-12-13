from typing import NamedTuple, List
import csv


class Country(NamedTuple):
    name: str
    alpha2: str
    alpha3: str
    numeric: str
    apolitical_name: str


def collect_country_data(fp: str) -> List[Country]:
    countries = []
    with open(fp, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader)  # Skip the header row
        for row in reader:
            if row:  # Ensure the row is not empty
                print(len(row))
                print(row)
                country = Country(*row)
                countries.append(country)
    return countries
