"""
Countries.py

Write the csv data to a a list of Country classes.
"""
from botech_metadata import _records


def main():
    output_path = 'botech_metadata/country_definitions.py'
    with open(output_path, 'w') as f:
        for record in _records:
            f.write(f'{record}\n')

# Usage
if __name__ == "__main__":
    main()
