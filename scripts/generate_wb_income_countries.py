#!/usr/bin/env python3

import json
import sys
from country_metadata import countries, get_tag

def generate_wb_income_countries():
    """Generate a JSON of countries grouped by World Bank income classification."""
    wb_income_countries = {}
    
    for country in countries:
        income_level = get_tag(country.alpha3, "wb_income")
        if income_level is not None:
            if income_level not in wb_income_countries:
                wb_income_countries[income_level] = []
            
            wb_income_countries[income_level].append({
                "name": country.name,
                "iso3": country.alpha3
            })
    
    # Sort countries within each income level alphabetically
    for income_level in wb_income_countries:
        wb_income_countries[income_level].sort(key=lambda x: x["name"])
    
    # Create final JSON structure
    output = {
        "countries_by_wb_income": wb_income_countries
    }
    
    return output

if __name__ == "__main__":
    # Generate the filtered country list
    wb_income_data = generate_wb_income_countries()
    
    # Output to stdout or file
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(wb_income_data, f, ensure_ascii=False, indent=4)
        print(f"Saved to {output_file}")
    else:
        # Print to stdout with nice formatting
        print(json.dumps(wb_income_data, ensure_ascii=False, indent=4))