import os
from dotenv import load_dotenv
from extract_data import extract_data
from transform import load_data_from_files, transform_data


load_dotenv()

if __name__ == "__main__":
    # Load environment variables
    ALL_CONTACTS_VIEW_ID = os.getenv('ALL_CONTACTS_VIEW_ID')
    ALL_ACCOUNTS_VIEW_ID = os.getenv('ALL_ACCOUNTS_VIEW_ID')
    ALL_DEALS_VIEW_ID = os.getenv('ALL_DEALS_VIEW_ID')
    OUTPUT_DIR = os.getenv('OUTPUT_DIR')

    # Create output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    #Extraction Phase
    extract_data("contacts", ALL_CONTACTS_VIEW_ID, OUTPUT_DIR)
    extract_data("sales_accounts", ALL_ACCOUNTS_VIEW_ID, OUTPUT_DIR)
    extract_data("deals", ALL_DEALS_VIEW_ID, OUTPUT_DIR)

    # Load and Transform Data Phase
    contacts_data, deals_data, accounts_data = load_data_from_files(OUTPUT_DIR)
    transform_data(contacts_data, deals_data, accounts_data)
