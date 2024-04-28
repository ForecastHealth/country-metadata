"""
__init__.py

Contains the API for interacting with botech-metadata
"""
from typing import Union, Optional, List, Dict, Tuple
from itertools import product
from .country import Country, countries
from .preprocessing import preprocess_country_name
from .tag import ACCEPTED_TAGS, Tag
from fuzzywuzzy import fuzz

def get_country(
    identifier: Union[str, int],
    threshold: int = 80
) -> Optional[Country]:
    if isinstance(identifier, str):
        identifier = preprocess_country_name(identifier)

    for country in countries:
        if isinstance(identifier, int):
            if country.numeric == identifier:
                return country
        else:
            preprocessed_name = preprocess_country_name(country.name)
            if (
                country.alpha2 == identifier
                or country.alpha3 == identifier
                or preprocessed_name.lower() == identifier.lower()
                or identifier.lower() in preprocessed_name.lower()
            ):
                return country

    # If no direct match is found, perform fuzzy matching
    best_match = None
    best_ratio = 0
    for country in countries:
        preprocessed_name = preprocess_country_name(country.name)
        ratio = fuzz.ratio(identifier.lower(), preprocessed_name.lower())
        if ratio > best_ratio:
            best_match = country
            best_ratio = ratio

    if best_ratio >= threshold:
        return best_match

    return None


def list_tags() -> List[Tuple[str, str]]:
    return [(tag.label, tag.description) for tag in ACCEPTED_TAGS]


def get_tag(identifier: str, tag_label: str) -> Optional[str]:
    country = get_country(identifier)
    if country is None:
        return None

    tag_instance = next((tag for tag in ACCEPTED_TAGS if tag.label == tag_label), None)
    if tag_instance is None:
        return None

    mapping_property = getattr(country, tag_instance.mapping_property, None)
    if mapping_property is not None:
        return tag_instance.data.get(mapping_property)

    return None


def get_countries_by_tags(*tags: str) -> Dict[str, List[Country]]:
    tag_mapping = {tag.label: tag for tag in ACCEPTED_TAGS}

    tags = [tag.lower() for tag in tags]
    for tag in tags:
        if tag not in tag_mapping:
            raise ValueError(f"Invalid category: {tag}")

    tag_sets = []
    for tag in tags:
        tag_instance = tag_mapping[tag]
        data_values = set(tag_instance.data.values())
        tag_sets.append(data_values)

    combinations = product(*tag_sets)

    result = {}
    for combo in combinations:
        combo_str = ', '.join(str(value) for value in combo)
        filtered_countries = [
            country
            for country in countries
            if all(tag_mapping[tag].data.get(getattr(country, tag_mapping[tag].mapping_property)) == value
                   for tag, value in zip(tags, combo))
        ]
        result[combo_str] = filtered_countries

    return result


__all__ = [
    "countries",
    "get_country",
    "get_tag",
    "get_countries_by_tags"
]
