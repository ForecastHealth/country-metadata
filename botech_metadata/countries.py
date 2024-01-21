from dataclasses import dataclass
from typing import NamedTuple, List
from .who_regions import ccn3_to_region
import csv


@dataclass
class Country:
    name: str
    alpha2: str
    alpha3: str
    numeric: str
    apolitical_name: str
    region: str = "No Region"
    income: str = "No Income Status"
    appendix_3: bool = False

    def __post_init__(self):
        self.who_region = ccn3_to_region.get(self.numeric, "No Region")


def collect_country_data(fp: str) -> List[Country]:
    countries = []
    with open(fp, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            country = Country(
                name=row.get('name'),
                alpha2=row.get('alpha2'),
                alpha3=row.get('alpha3'),
                numeric=row.get('numeric'),
                apolitical_name=row.get('apolitical_name'),
                region=row.get('region') or 'No Region',
                income=row.get('income') or 'No Income',
                appendix_3=get_appendix_3_value(row)
            )
            countries.append(country)
    return countries


def get_appendix_3_value(row: dict) -> str:
    value = row.get('appendix_3')
    if not value:
        return 'Not in Appendix 3'
    else:
        return "In Appendix 3"
    
