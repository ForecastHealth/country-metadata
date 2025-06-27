#!/usr/bin/env python3

import json
import sys
from country_metadata import countries, get_tag

def generate_who_region_countries():
    """Generate a JSON of countries grouped by WHO region classification."""
    who_region_countries = {}
    
    for country in countries:
        region = get_tag(country.numeric, "who_region")
        if region is not None:
            if region not in who_region_countries:
                who_region_countries[region] = []
            
            who_region_countries[region].append({
                "name": country.name,
                "iso3": country.alpha3
            })
    
    # Sort countries within each region alphabetically
    for region in who_region_countries:
        who_region_countries[region].sort(key=lambda x: x["name"])
    
    # Create final JSON structure
    output = {
        "countries_by_who_region": who_region_countries
    }
    
    return output

if __name__ == "__main__":
    # Generate the filtered country list
    who_region_data = generate_who_region_countries()
    
    # Output to stdout or file
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(who_region_data, f, ensure_ascii=False, indent=4)
        print(f"Saved to {output_file}")
    else:
        # Print to stdout with nice formatting
        print(json.dumps(who_region_data, ensure_ascii=False, indent=4))