"""
metadata.py

Open up the class, print some stuff.
"""
import sys
import pprint
from botech_metadata import countries


def main():
    idx = sys.argv[1]
    # query = sys.argv[2]
    pprint.pprint(countries.countries_by_category(idx).keys())


if __name__ == "__main__":
    main()
