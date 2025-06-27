#!/usr/bin/env python3

import json
import sys
from country_metadata import countries, get_tag

def generate_wb_region_countries():
    """Generate a JSON of countries grouped by World Bank region classification."""
    wb_region_countries = {}
    
    for country in countries:
        region = get_tag(country.alpha3, "wb_region")
        if region is not None:
            if region not in wb_region_countries:
                wb_region_countries[region] = []
            
            wb_region_countries[region].append({
                "name": country.name,
                "iso3": country.alpha3
            })
    
    # Sort countries within each region alphabetically
    for region in wb_region_countries:
        wb_region_countries[region].sort(key=lambda x: x["name"])
    
    # Create final JSON structure
    output = {
        "countries_by_wb_region": wb_region_countries
    }
    
    return output

if __name__ == "__main__":
    # Generate the filtered country list
    wb_region_data = generate_wb_region_countries()
    
    # Output to stdout or file
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(wb_region_data, f, ensure_ascii=False, indent=4)
        print(f"Saved to {output_file}")
    else:
        # Print to stdout with nice formatting
        print(json.dumps(wb_region_data, ensure_ascii=False, indent=4))