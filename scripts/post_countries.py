#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
post_countries.py

Script to post all countries with their metadata to the API.
Iterates through all actual countries from the country_metadata package,
retrieves their metadata including tags, and posts them to the API endpoint.
"""
import os
import requests
import logging
import json
from dotenv import load_dotenv
import country_metadata

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# List of tags to fetch for each country
TAGS_TO_FETCH = ["wb_income", "wb_region", "appendix_3", "who_region"]

# Non-country alpha3 codes to filter out
NON_COUNTRY_ALPHA3 = [
    "ZZZ",  # World
    "AFR", "PAH", "EMR", "EUR", "SEA", "WPR",  # WHO Regions
    "HIG", "UPP", "LMI", "LOW"  # WB Income Regions
]


def get_country_payload(country):
    """
    Create API payload for a country.
    
    Args:
        country: A country_metadata.Country object
        
    Returns:
        dict: API payload or None if not a real country
    """
    # Filter out non-countries
    if (len(country.alpha3) != 3 or
            not country.alpha3.isupper() or
            country.alpha3.startswith('ZZ') or
            country.alpha3 in NON_COUNTRY_ALPHA3):
        return None
    
    # Initialize payload with basic country fields
    payload = {
        "iso3": country.alpha3,
        "name": country.name,
        "alpha2": country.alpha2,
        "numericCode": country.numeric,
        "apoliticalName": country.apolitical_name
    }
    
    # Fetch tag data
    for tag in TAGS_TO_FETCH:
        # Use numeric for who_region, alpha3 for others
        identifier = country.numeric if tag == "who_region" else country.alpha3
        tag_value = country_metadata.get_tag(identifier, tag)
        
        if tag_value is not None:
            if tag == "wb_income":
                payload["wbIncomeLevel"] = tag_value
            elif tag == "wb_region":
                payload["wbRegion"] = tag_value
            elif tag == "appendix_3":
                payload["appendix3"] = bool(tag_value)  # Convert 1/0 to True/False
            elif tag == "who_region":
                payload["whoRegion"] = tag_value
        else:
            logging.warning(f"Missing tag '{tag}' for country {country.alpha3}")
    
    return payload


def main():
    """Main function to execute the script."""
    # Load environment variables
    load_dotenv()
    
    # Retrieve API base URL from environment
    api_base_url = os.getenv("API_BASE_URL")
    if not api_base_url:
        logging.error("API_BASE_URL environment variable is not set. Please set it in .env file.")
        return
    
    # Construct endpoint URL
    post_endpoint = f"{api_base_url.rstrip('/')}/v1/countries/"
    logging.info(f"Starting country data posting to: {post_endpoint}")
    
    # Get all countries
    all_countries = country_metadata.countries
    
    # Initialize counters
    success_count = 0
    error_count = 0
    skipped_count = 0
    
    # Process each country
    for country in all_countries:
        logging.info(f"Processing country: {country.alpha3}")
        
        # Get payload for this country
        payload = get_country_payload(country)
        
        # Skip if not a valid country
        if payload is None:
            logging.info(f"Skipping {country.alpha3} (not a standard country)")
            skipped_count += 1
            continue
        
        # Make API request
        try:
            response = requests.post(
                post_endpoint,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            # Check response status
            if response.status_code == 201:
                logging.info(f"Successfully posted {country.alpha3}. Status: {response.status_code}")
                success_count += 1
            else:
                logging.error(
                    f"Failed to post {country.alpha3}. Status: {response.status_code}. "
                    f"Response: {response.text}"
                )
                error_count += 1
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error posting {country.alpha3}: {e}")
            error_count += 1
    
    # Log summary
    logging.info(f"Posting complete. Summary:")
    logging.info(f"  - Total countries processed: {len(all_countries)}")
    logging.info(f"  - Successfully posted: {success_count}")
    logging.info(f"  - Errors: {error_count}")
    logging.info(f"  - Skipped (non-countries): {skipped_count}")


if __name__ == "__main__":
    main()