import requests
import os

def extract_data(entity, view_id, output_dir):
    FRESHSALES_API_KEY = os.getenv('FRESHSALES_API_KEY')
    SALES_BUNDLE_ALIAS = os.getenv('SALES_BUNDLE_ALIAS')

    if not FRESHSALES_API_KEY or not SALES_BUNDLE_ALIAS:
        raise ValueError("FRESHSALES_API_KEY or SALES_BUNDLE_ALIAS environment variable is missing.")

    url = f"https://{SALES_BUNDLE_ALIAS}/api/{entity}/view/{view_id}"
    headers = {
        "Authorization": f"Token token={FRESHSALES_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        output_file = f"{output_dir}/{entity}.json"
        with open(output_file, "w") as file:
            file.write(response.text)
        print(f"Successfully extracted data for {entity} to {output_file}")
    else:
        print(f"Failed to extract data for {entity}. Status Code: {response.status_code}")
