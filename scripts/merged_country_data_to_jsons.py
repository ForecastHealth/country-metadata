import csv
import json

# Read the CSV file
csv_file = './data/merged_country_data.csv'  # Replace with your actual file path

region_dict = {}
income_dict = {}
appendix_3_dict = {}

with open(csv_file, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        alpha3 = row['alpha3']
        region_dict[alpha3] = row['region']
        income_dict[alpha3] = row['income']
        appendix_3_dict[alpha3] = row['appendix_3']

# Export to JSON
with open('./data/region.json', 'w', encoding='utf-8') as f:
    json.dump(region_dict, f, ensure_ascii=False, indent=4)

with open('./data/income.json', 'w', encoding='utf-8') as f:
    json.dump(income_dict, f, ensure_ascii=False, indent=4)

with open('./data/appendix_3.json', 'w', encoding='utf-8') as f:
    json.dump(appendix_3_dict, f, ensure_ascii=False, indent=4)
