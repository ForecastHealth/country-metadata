"""
metadata.py

Open up the class, print some stuff.
"""
import sys
import pprint
from botech_metadata import countries


def main():
    args = sys.argv[1:]
    pprint.pprint(countries.countries_by_categories(*args))


if __name__ == "__main__":
    main()
