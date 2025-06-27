#!/usr/bin/env python3

import json
import os
import sys
from pathlib import Path
from country_metadata import countries, get_tag

def sanitize_filename(name):
    """Convert tag values to safe filenames."""
    # Replace spaces and special characters with underscores
    safe_name = name.lower().replace(' ', '_').replace('&', 'and').replace(',', '')
    # Remove any other problematic characters
    safe_name = ''.join(c for c in safe_name if c.isalnum() or c in '_-')
    return safe_name

def generate_all_country_lists(output_dir='country_lists'):
    """Generate individual JSON files for each tag value across all tags."""
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(exist_ok=True)
    
    # Track all generated files
    generated_files = []
    
    # Process appendix_3 tag (binary)
    appendix_3_countries = []
    for country in countries:
        if get_tag(country.alpha3, "appendix_3") == 1:
            appendix_3_countries.append({
                "name": country.name,
                "iso3": country.alpha3
            })
    
    appendix_3_countries.sort(key=lambda x: x["name"])
    output_file = os.path.join(output_dir, "appendix_3.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({"countries": appendix_3_countries}, f, ensure_ascii=False, indent=4)
    generated_files.append(output_file)
    
    # Process wb_income tag
    wb_income_groups = {}
    for country in countries:
        income_level = get_tag(country.alpha3, "wb_income")
        if income_level is not None:
            if income_level not in wb_income_groups:
                wb_income_groups[income_level] = []
            wb_income_groups[income_level].append({
                "name": country.name,
                "iso3": country.alpha3
            })
    
    for income_level, country_list in wb_income_groups.items():
        country_list.sort(key=lambda x: x["name"])
        filename = f"wb_income_{sanitize_filename(income_level)}.json"
        output_file = os.path.join(output_dir, filename)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({"countries": country_list}, f, ensure_ascii=False, indent=4)
        generated_files.append(output_file)
    
    # Process wb_region tag
    wb_region_groups = {}
    for country in countries:
        region = get_tag(country.alpha3, "wb_region")
        if region is not None:
            if region not in wb_region_groups:
                wb_region_groups[region] = []
            wb_region_groups[region].append({
                "name": country.name,
                "iso3": country.alpha3
            })
    
    for region, country_list in wb_region_groups.items():
        country_list.sort(key=lambda x: x["name"])
        filename = f"wb_region_{sanitize_filename(region)}.json"
        output_file = os.path.join(output_dir, filename)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({"countries": country_list}, f, ensure_ascii=False, indent=4)
        generated_files.append(output_file)
    
    # Process who_region tag
    who_region_groups = {}
    for country in countries:
        region = get_tag(country.numeric, "who_region")
        if region is not None:
            if region not in who_region_groups:
                who_region_groups[region] = []
            who_region_groups[region].append({
                "name": country.name,
                "iso3": country.alpha3
            })
    
    for region, country_list in who_region_groups.items():
        country_list.sort(key=lambda x: x["name"])
        filename = f"who_region_{sanitize_filename(region)}.json"
        output_file = os.path.join(output_dir, filename)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({"countries": country_list}, f, ensure_ascii=False, indent=4)
        generated_files.append(output_file)
    
    return generated_files

if __name__ == "__main__":
    # Get output directory from command line or use default
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "country_lists"
    
    # Generate all country lists
    generated_files = generate_all_country_lists(output_dir)
    
    print(f"Generated {len(generated_files)} country list files in '{output_dir}':")
    for file_path in sorted(generated_files):
        print(f"  - {file_path}")