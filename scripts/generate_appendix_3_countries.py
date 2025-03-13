#!/usr/bin/env python3

import json
import sys
from country_metadata import countries, get_tag

def generate_appendix_3_countries():
    """Generate a JSON of countries where appendix_3 tag equals 1."""
    appendix_3_countries = []
    
    for country in countries:
        if get_tag(country.alpha3, "appendix_3") == 1:
            appendix_3_countries.append({
                "name": country.name,
                "iso3": country.alpha3
            })
    
    # Sort countries by name alphabetically
    appendix_3_countries.sort(key=lambda x: x["name"])
    
    # Create final JSON structure
    output = {
        "countries": appendix_3_countries
    }
    
    return output

if __name__ == "__main__":
    # Generate the filtered country list
    appendix_3_data = generate_appendix_3_countries()
    
    # Output to stdout or file
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(appendix_3_data, f, ensure_ascii=False, indent=4)
        print(f"Saved to {output_file}")
    else:
        # Print to stdout with nice formatting
        print(json.dumps(appendix_3_data, ensure_ascii=False, indent=4))