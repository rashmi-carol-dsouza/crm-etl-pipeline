import os
from dotenv import load_dotenv
from extract_data import extract_data
from transform import load_data_from_files, transform_data
from calculate_aggregations import calculate_aggregates, generate_contacts_per_account


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

    # Ingest and Transform Data Phase
    contacts_data, deals_data, accounts_data = load_data_from_files(OUTPUT_DIR)
    contacts_df, deals_df, accounts_df = transform_data(contacts_data, deals_data, accounts_data)
    contacts_df.to_csv("contacts.csv", index=False)
    deals_df.to_csv("deals.csv", index=False)
    accounts_df.to_csv("accounts.csv", index=False)

    # # Aggregation Phase
    # aggregated_metrics = calculate_aggregates(deals_df, contacts_df, accounts_df)
    # contacts_per_account = generate_contacts_per_account(contacts_df)

    # # Print for Verification
    # for agg_type, df in aggregated_metrics.items():
    #     print(f"{agg_type}:")
    #     print(df)

    # print("\nContacts Per Account:")
    # print(contacts_per_account)
