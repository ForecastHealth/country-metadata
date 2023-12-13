# -*- coding: utf-8 -*-

import re
from typing import Dict, Iterator, Type, TypeVar, Union, overload
from botech_metadata.countries import Country, collect_country_data

__all__ = ["countries"]

StrOrInt = Union[str, int]
_D = TypeVar("_D")


_records = collect_country_data("botech_metadata/country_records.csv")


def _build_index(idx: int) -> Dict[str, Country]:
    return dict((r[idx].upper(), r) for r in _records)


# Internal country indexes
_by_alpha2 = _build_index(1)
_by_alpha3 = _build_index(2)
_by_numeric = _build_index(3)
_by_name = _build_index(0)
_by_apolitical_name = _build_index(4)


# Documented accessors for the country indexes
countries_by_alpha2 = _by_alpha2
countries_by_alpha3 = _by_alpha3
countries_by_numeric = _by_numeric
countries_by_name = _by_name
countries_by_apolitical_name = _by_apolitical_name


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
            else:
                r = _by_apolitical_name.get(k, default)

        if r == NotFound:
            raise KeyError(key)

        return r

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
