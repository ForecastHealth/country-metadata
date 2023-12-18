# -*- coding: utf-8 -*-

import re
from typing import Dict, List, Iterator, Type, TypeVar, Union, overload
from .countries import Country, collect_country_data
from .country_definitions import country_definitions
from itertools import product

__all__ = ["countries"]

StrOrInt = Union[str, int]
_D = TypeVar("_D")


# _records = collect_country_data("botech_metadata/merged_country_data.csv")
_records = country_definitions


def _build_index(idx: int, is_bool: bool = False) -> Dict[str, Country]:
    if is_bool:
        return dict((str(r[idx]), r) for r in _records)
    else:
        return dict((r[idx].upper(), r) for r in _records)


# Internal country indexes
_by_alpha2 = _build_index(1)
_by_alpha3 = _build_index(2)
_by_numeric = _build_index(3)
_by_name = _build_index(0)
_by_apolitical_name = _build_index(4)
_by_region = _build_index(5)
_by_income = _build_index(6)
_by_appendix_3 = _build_index(7, is_bool=True)


# Documented accessors for the country indexes
countries_by_alpha2 = _by_alpha2
countries_by_alpha3 = _by_alpha3
countries_by_numeric = _by_numeric
countries_by_name = _by_name
countries_by_apolitical_name = _by_apolitical_name
countries_by_region = _by_region
countries_by_income = _by_income
countries_by_appendix_3 = _by_appendix_3


class NotFound:
    pass


class _CountryLookup:
    @overload
    def get(self, key: StrOrInt) -> Country:
        ...

    @overload
    def get(self, key: StrOrInt, default: _D) -> Union[Country, _D]:
        ...

    def get(
        self, key: StrOrInt, default: Union[Type[NotFound], _D] = NotFound
    ) -> Union[Country, _D]:
        if isinstance(key, int):
            k = f"{key:03d}"
            r = _by_numeric.get(k, default)
        else:
            k = key.upper()
            if len(k) == 2:
                r = _by_alpha2.get(k, default)
            elif len(k) == 3 and re.match(r"[0-9]{3}", k) and k != "000":
                r = _by_numeric.get(k, default)
            elif len(k) == 3:
                r = _by_alpha3.get(k, default)
            elif k in _by_name:
                r = _by_name.get(k, default)
            elif k in _by_region:
                r = _by_region.get(k, default)
            elif k in _by_income:
                r = _by_income.get(k, default)
            elif k in _by_appendix_3:
                r = _by_appendix_3.get(k, default)
            else:
                r = _by_apolitical_name.get(k, default)

        if r == NotFound:
            raise KeyError(key)

        return r

    def find_by(self, index: str, query: str) -> List[Country]:
        """
        Find countries based on a given index and query.

        Args:
            index (str): The index to search by (e.g., 'alpha3', 'region').
            query (str): The query value to match against the index.

        Returns:
            List[Country]: A list of countries that match the query in the specified index.
        """
        query = query.upper()
        if index == 'alpha2':
            return [country for country in _records if country.alpha2.upper() == query]
        elif index == 'alpha3':
            return [country for country in _records if country.alpha3.upper() == query]
        elif index == 'numeric':
            return [country for country in _records if country.numeric == query]
        elif index == 'name':
            return [country for country in _records if country.name.upper() == query]
        elif index == 'apolitical_name':
            return [country for country in _records if country.apolitical_name.upper() == query]
        elif index == 'region':
            return [country for country in _records if country.region.upper() == query]
        elif index == 'income':
            return [country for country in _records if country.income.upper() == query]
        elif index == 'appendix_3':
            query_bool = query.lower() in ["true", "1", "yes"]
            return [country for country in _records if country.appendix_3 == query_bool]  
        else:
            raise ValueError(f"Invalid index: {index}")

    def countries_by_category(self, category: str) -> Dict[str, List[Country]]:
        result = {}
        if category == 'region':
            for country in _records:
                region = country.region.upper()
                if region not in result:
                    result[region] = []
                result[region].append(country)
        elif category == 'income':
            for country in _records:
                income = country.income.upper()
                if income not in result:
                    result[income] = []
                result[income].append(country)
        elif category == 'appendix_3':
            for country in _records:
                appendix_3 = country.appendix_3
                if appendix_3 not in result:
                    result[appendix_3] = []
                result[appendix_3].append(country)
        return result

    def countries_by_categories(self, *categories: str) -> Dict[str, List[Country]]:
        """
        Generate combinatorics of countries based on provided categories.

        Args:
            *categories (str): Variable number of category arguments like 'region', 'income', 'appendix_3'.

        Returns:
            Dict[str, List[Country]]: A dictionary with keys as category combinations and values as lists of countries.
        """
        categories = [cat.lower() for cat in categories]
        valid_categories = ['region', 'income', 'appendix_3']
        for cat in categories:
            if cat not in valid_categories:
                raise ValueError(f"Invalid category: {cat}")

        # Create a list of sets for each category
        category_sets = [set(getattr(country, cat) for country in _records) for cat in categories]

        # Generate all possible combinations
        combinations = product(*category_sets)

        # Prepare the result dictionary
        result = {}
        for combo in combinations:
            # Convert all elements of combo to strings
            combo_str = ', '.join(str(value) for value in combo)
            filtered_countries = [country for country in _records if all(getattr(country, cat) == value for cat, value in zip(categories, combo))]
            result[combo_str] = filtered_countries
        return result

    __getitem__ = get

    def __len__(self) -> int:
        return len(_records)

    def __iter__(self) -> Iterator[Country]:
        return iter(_records)

    def __contains__(self, item: StrOrInt) -> bool:
        try:
            self.get(item)
            return True
        except KeyError:
            return False


countries = _CountryLookup()
