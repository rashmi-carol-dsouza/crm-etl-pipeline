import requests
from dotenv import load_dotenv
import os

load_dotenv()

FRESHSALES_API_KEY = os.getenv('FRESHSALES_API_KEY')
SALES_BUNDLE_ALIAS = os.getenv('SALES_BUNDLE_ALIAS')
ALL_CONTACTS_VIEW_ID = os.getenv('ALL_CONTACTS_VIEW_ID')
ALL_ACCOUNTS_VIEW_ID = os.getenv('ALL_ACCOUNTS_VIEW_ID')
ALL_DEALS_VIEW_ID = os.getenv('ALL_DEALS_VIEW_ID')
OUTPUT_DIR = os.getenv('OUTPUT_DIR')

def extract_data(entity, view_id, output_file):
    url = f"https://{SALES_BUNDLE_ALIAS}/api/{entity}/view/{view_id}"
    headers = {
        "Authorization": f"Token token={FRESHSALES_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        with open(f'{OUTPUT_DIR}/{output_file}', "w") as file:
            file.write(response.text)
        print(f"Successfully extracted data for {entity} to {output_file}")


if __name__ == "__main__":
    # Extract contacts, accounts, and deals data using the corresponding view IDs
    extract_data("contacts", ALL_CONTACTS_VIEW_ID, "contacts.json")
    extract_data("sales_accounts", ALL_ACCOUNTS_VIEW_ID, "accounts.json")
    extract_data("deals", ALL_DEALS_VIEW_ID, "deals.json")