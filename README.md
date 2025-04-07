# country-metadata
A small python library containing methods to access data about countries.

# set-up
```bash
git clone https://github.com/ForecastHealth/country-metadata.git
cd country-metadata
pip install .
```

# Scripts
The repository contains several utility scripts in the `scripts/` directory:

## post_countries.py
This script posts all countries with their metadata to an API endpoint. It:
- Iterates through all actual countries (filtering out non-countries)
- Retrieves their metadata including tags (wbRegion, wbIncomeLevel, appendix3, whoRegion)
- Posts each country to the API endpoint

Usage:
```bash
# First, create a .env file with your API URL (see .env.example)
cp .env.example .env
# Edit the .env file with your actual API URL
nano .env

# Install required dependencies
pip install python-dotenv requests

# Run the script
python scripts/post_countries.py
```

# Basic Features
## Country
There is a list of countries which are hard coded, and contain the following information:

name: The name of the country in English.
alpha2: The two-letter country code.
    Also referred to as ISO2 or CCA2
alpha3: The three-letter country code.
    Also referred to as ISO3 or CCA3
numeric: The numeric country code.
    Also referred to as UNSDM49 or CCN3
apolitical_name: The name of the country in English, without any political connotations.

## Tag
A tag is an optional piece of information that can be associated with a country. Importantly, tags are not unique, and may be missing. Therefore, tags can be useful to group countries in useful ways e.g. country regions, income levels etc.

Tags are designed to be extensible, and should be straightforward to adapt using definitions found in `./country_metadata/tag.py` and examples in `./country_metadata/tags/`.

# API
The API is defined in `./country_metadata/__init__.py` and has can be used as follows:
```python
import country_metadata as cm
>> cm.get('AUS')
Country(name='Australia', alpha2='AU', alpha3='AUS', numeric=36, apolitical_name='Australia')

>> for tag in cm.list_tags():
>>    print(tag)
('appendix_3', 'Whether or not Appendix 3 appeared in the 2022 WHO NCD Appendix 3 analysis.')
('wb_income', "The World Bank's income level classification.")
('wb_region', "The World Bank's region classification.")
('who_region', 'The WHO region classification.')

>> cm.get_tag('AUS', 'wb_income')
'High Income'
```

# Fork
This project was originally forked from [deactivated/python-iso3166](https://github.com/deactivated/python-iso3166), and it has retained the basic information retained in the `Country` dataclass. However, the API is completely new. We have retained the original LICENSE.
