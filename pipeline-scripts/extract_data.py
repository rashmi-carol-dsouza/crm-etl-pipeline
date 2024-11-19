import requests
import os
import json

def extract_data(entity, view_id, output_dir):
    FRESHSALES_API_KEY = os.getenv('FRESHSALES_API_KEY')
    SALES_BUNDLE_ALIAS = os.getenv('SALES_BUNDLE_ALIAS')

    if not FRESHSALES_API_KEY or not SALES_BUNDLE_ALIAS:
        raise ValueError("FRESHSALES_API_KEY or SALES_BUNDLE_ALIAS environment variable is missing.")

    page = 1
    all_data = []

    while True:
        url = f"https://{SALES_BUNDLE_ALIAS}/api/{entity}/view/{view_id}?page={page}"
        headers = {
            "Authorization": f"Token token={FRESHSALES_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            all_data.extend(data[entity])

            # Check if there are more pages
            if page >= data.get('meta', {}).get('total_pages', 1):
                break
            page += 1
        else:
            print(f"Failed to extract data for {entity}. Status Code: {response.status_code}")
            break

    output_file = f"{output_dir}/{entity}.json"
    with open(output_file, "w") as file:
        json.dump(all_data, file)
    print(f"Successfully extracted data for {entity} to {output_file}")

extract_data("contacts", os.getenv('ALL_CONTACTS_VIEW_ID'), os.getenv('OUTPUT_DIR'))