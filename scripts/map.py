"""
map_income_and_region.py
"""
import pandas as pd


def main():
    metadata_df = pd.read_csv("data/country_metadata.csv")
    records_df = pd.read_csv("botech_metadata/country_records.csv")
    merged_df = pd.merge(records_df, metadata_df, left_on='alpha3', right_on='iso3', how='left')
    final_df = merged_df[['name', 'alpha2', 'alpha3', 'numeric', 'apolitical_name', 'region', 'income_group', 'is_appendix3']]
    final_df.to_csv("botech_metadata/merged_country_data.csv", index=False)


if __name__ == "__main__":
    main()
