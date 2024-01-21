"""
tag.py

Methods to add additional tags to the metadata.
Tags are used to group countries together based on some information,
e.g. region, income level etc.

They are not unique and can be missing.
"""
from dataclasses import dataclass
from .tags import (
    iso3_to_appendix_3,
    iso3_to_wb_income_level,
    iso3_to_wb_region,
    ccn3_to_who_region,
)

@dataclass
class Tag:
    label: str
    description: str
    mapping_property: str
    data: dict


ACCEPTED_TAGS = [
    Tag(
        label="appendix_3",
        description="""
        Whether or not Appendix 3 appeared in the 2022 WHO NCD Appendix 3 analysis.
        A 1 indicates that the country appeared in the analysis,
        a 0 indicates that it did not
        """,
        mapping_property="alpha3",
        data=iso3_to_appendix_3
    ),
    Tag(
        label="wb_income",
        description="The World Bank's income level classification.",
        mapping_property="alpha3",
        data=iso3_to_wb_income_level
    ),
    Tag(
        label="wb_region",
        description="The World Bank's region classification.",
        mapping_property="alpha3",
        data=iso3_to_wb_region
    ),
    Tag(
        label="who_region",
        description="",
        mapping_property="numeric",
        data=ccn3_to_who_region
    )
]


