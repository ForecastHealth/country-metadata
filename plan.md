Okay, let's break down the plan for creating the `scripts/post_countries.py` script.

**Goal:** Create a Python script (`./scripts/post_countries.py`) that iterates through all *actual* countries defined in the `botech_metadata` package, retrieves their basic information and relevant tags (wbRegion, wbIncomeLevel, appendix3, whoRegion) using the package's API, formats this data according to the provided Swagger definition for the POST endpoint, and sends a POST request for each country to the `API_BASE_URL/v1/countries/` endpoint.

**Input Analysis:**

1.  **`botech_metadata` Package:**
    *   Provides a list of `Country` objects via `botech_metadata.countries`. Each object has `name`, `alpha2`, `alpha3`, `numeric`, `apolitical_name`.
    *   Provides functions to get tag data, specifically `botech_metadata.get_tag(identifier, tag_label)`.
    *   Tag data (`wb_region`, `wb_income`, `appendix_3`, `who_region`) is stored internally and mapped using either `alpha3` or `numeric` codes.
    *   The `countries` list includes non-country entities (World, WHO Regions, Income Levels) which likely need to be filtered out.
2.  **Swagger Excerpt (POST `/v1/countries/`):**
    *   Defines the required JSON structure for the POST request body.
    *   Specifies field names (`iso3`, `name`, `alpha2`, `numericCode`, `apoliticalName`, `wbIncomeLevel`, `wbRegion`, `appendix3`, `whoRegion`) and expected types (string, number, boolean).
    *   Highlights potential differences in field names (e.g., `numeric` vs `numericCode`, `apolitical_name` vs `apoliticalName`) and types (`appendix_3` integer vs `appendix3` boolean).
3.  **`.env` File:**
    *   Contains the `API_BASE_URL` variable required to construct the full API endpoint URL.

**Implementation Plan for `./scripts/post_countries.py`**

1.  **File Setup:**
    *   Create the file `./scripts/post_countries.py`.
    *   Add standard script headers (e.g., `#!/usr/bin/env python3`, encoding declaration).
    *   Add a docstring explaining the script's purpose.

2.  **Import Necessary Libraries:**
    *   `os`: To interact with the operating system (potentially for environment variables, though `dotenv` is better).
    *   `requests`: For making HTTP POST requests.
    *   `dotenv`: To load environment variables from the `.env` file (specifically `API_BASE_URL`). Use `load_dotenv()`.
    *   `logging`: For informative output during script execution.
    *   `botech_metadata`: The package itself to access country data and tag functions (`countries`, `get_tag`).
    *   `json`: Although `requests` handles JSON serialization, it might be useful for debugging payloads.

3.  **Configuration and Constants:**
    *   Load environment variables using `dotenv.load_dotenv()`.
    *   Retrieve `API_BASE_URL` from environment variables: `api_base_url = os.getenv("API_BASE_URL")`. Add error handling if it's not set.
    *   Construct the full target endpoint URL: `post_endpoint = f"{api_base_url.rstrip('/')}/v1/countries/"`.
    *   Define the list of tags to retrieve for each country: `TAGS_TO_FETCH = ["wb_income", "wb_region", "appendix_3", "who_region"]`.
    *   Configure `logging`: Set up a basic logger (e.g., `logging.basicConfig`) to output INFO level messages to the console, including timestamps and log levels.

4.  **Define Helper Functions (Optional but Recommended):**
    *   `get_country_payload(country: botech_metadata.Country) -> Optional[dict]:`
        *   Takes a `botech_metadata.Country` object as input.
        *   **Filter Non-Countries:** Check if the country is a "real" country. A simple check could be `if len(country.alpha3) == 3 and country.alpha3.isupper() and not country.alpha3.startswith('ZZ') and not country.alpha3 in ['AFR', 'PAH', 'EMR', 'EUR', 'SEA', 'WPR', 'HIG', 'UPP', 'LMI', 'LOW']:` (Adjust filter as needed based on `country.py`). If not a real country, return `None`.
        *   Initialize an empty dictionary `payload = {}`.
        *   **Map Basic Fields:**
            *   `payload["iso3"] = country.alpha3`
            *   `payload["name"] = country.name`
            *   `payload["alpha2"] = country.alpha2`
            *   `payload["numericCode"] = country.numeric`
            *   `payload["apoliticalName"] = country.apolitical_name`
        *   **Fetch and Map Tag Fields:** Iterate through `TAGS_TO_FETCH`:
            *   Call `tag_value = botech_metadata.get_tag(country.alpha3 if tag != "who_region" else country.numeric, tag)`. (Use `numeric` for `who_region`, `alpha3` for others based on `tag.py` inspection).
            *   **Handle Missing Tags:** If `tag_value` is not `None`:
                *   If `tag == "wb_income"`: `payload["wbIncomeLevel"] = tag_value`
                *   If `tag == "wb_region"`: `payload["wbRegion"] = tag_value`
                *   If `tag == "appendix_3"`: `payload["appendix3"] = bool(tag_value)` # Convert 1/0 to True/False
                *   If `tag == "who_region"`: `payload["whoRegion"] = tag_value`
            *   Else (if `tag_value` is `None`), log a warning that the tag is missing for this country, but continue building the payload (the API should handle missing optional fields). Or, explicitly set to `None` if the API requires it: `payload[<api_field_name>] = None`. *Decision: Assume API handles missing optional fields, so just don't add the key if the value is None.*
        *   Return the `payload` dictionary.

5.  **Main Execution Logic (`main` function):**
    *   Define a `main()` function.
    *   Log the start of the script and the target API endpoint.
    *   Retrieve the list of all country objects: `all_countries = botech_metadata.countries`.
    *   Initialize counters: `success_count = 0`, `error_count = 0`, `skipped_count = 0`.
    *   Iterate through `all_countries`: `for country in all_countries:`
        *   Log which country is being processed (e.g., using `country.alpha3`).
        *   Call `payload = get_country_payload(country)`.
        *   **Check if Skipped:** If `payload is None`:
            *   Log that the entry is being skipped (not a standard country).
            *   `skipped_count += 1`
            *   `continue` to the next iteration.
        *   **Make API Request:**
            *   Use a `try...except` block to handle potential `requests.exceptions.RequestException` (network errors, timeouts etc.).
            *   Inside the `try`:
                *   `response = requests.post(post_endpoint, json=payload, headers={"Content-Type": "application/json"}, timeout=30)` # Add a timeout
                *   **Check Response Status:**
                    *   If `response.status_code == 201`:
                        *   Log success (e.g., f"Successfully posted {country.alpha3}. Status: {response.status_code}").
                        *   `success_count += 1`
                    *   Else (e.g., 400, 409, 500):
                        *   Log an error including the status code, country ISO3, and the response body: `logging.error(f"Failed to post {country.alpha3}. Status: {response.status_code}. Response: {response.text}")`.
                        *   `error_count += 1`
            *   Inside the `except requests.exceptions.RequestException as e:`:
                *   Log the network error: `logging.error(f"Network error posting {country.alpha3}: {e}")`.
                *   `error_count += 1`
        *   **(Optional) Add Delay:** If concerned about rate limiting, add `time.sleep(0.1)` here.
    *   Log summary statistics: Total processed, successful posts, errors, skipped entries.

6.  **Script Entry Point:**
    *   Use the standard `if __name__ == "__main__":` block to call the `main()` function.

7.  **Dependencies:**
    *   Create a `requirements.txt` (or similar) if needed, listing:
        *   `requests`
        *   `python-dotenv`
        *   The `botech_metadata` package itself (needs to be installable, e.g., `pip install -e .` if running from the repo root).

8.  **`.env` File:**
    *   Ensure a `.env` file exists in the project root (or wherever `load_dotenv` expects it) with the line:
        `API_BASE_URL=http://your-api-base-url.com` (Replace with the actual URL).

**Self-Correction/Refinement during Planning:**

*   **Field Name Mapping:** Explicitly noted the mapping from package names (`numeric`, `apolitical_name`) to API names (`numericCode`, `apoliticalName`).
*   **Type Conversion:** Explicitly noted the conversion for `appendix3` from integer (1/0) in the package's tag data to boolean (`True`/`False`) for the API.
*   **Identifier for `get_tag`:** Realized `who_region` uses `numeric` code (ccn3) while others use `alpha3` (iso3) based on the tag data files (`tags/who_region.py` vs others) and `tag.py` mapping property. Adjusted the call accordingly.
*   **Filtering Non-Countries:** Added a specific step and logic within `get_country_payload` to identify and skip non-country entities present in `botech_metadata.countries`.
*   **Error Handling:** Included specific checks for response status codes and network exceptions (`requests.exceptions.RequestException`). Added detailed error logging.
*   **Optional Fields:** Decided initially to omit keys for missing tags rather than sending `null`, assuming the API treats missing optional fields correctly. This might need adjustment based on actual API behavior.
*   **Clarity:** Used function (`get_country_payload`) to encapsulate the logic for preparing data for a single country, improving readability of the main loop.

This detailed plan provides a clear roadmap for an LLM agent (or human developer) to implement the `post_countries.py` script.