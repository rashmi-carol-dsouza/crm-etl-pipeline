import sqlalchemy
import os
from dotenv import load_dotenv
from extract_data import extract_data, extract_sales_accounts
from transform import load_data_from_files, transform_data
from calculate_aggregations import calculate_aggregates, generate_contacts_per_account
from load import load_dataframe_to_postgres
from kpis import aggregate_deals_per_contact,aggregated_contacts_per_account,contacts_list


load_dotenv()

if __name__ == "__main__":
    print("Loading env variables")
    # Load environment variables
    ALL_CONTACTS_VIEW_ID = os.getenv('ALL_CONTACTS_VIEW_ID')
    ALL_ACCOUNTS_VIEW_ID = os.getenv('ALL_ACCOUNTS_VIEW_ID')
    ALL_DEALS_VIEW_ID = os.getenv('ALL_DEALS_VIEW_ID')
    OUTPUT_DIR = os.getenv('OUTPUT_DIR')

    # Create output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    #Extraction Phase
    print("Extracting data...")
    extract_data("contacts", ALL_CONTACTS_VIEW_ID, OUTPUT_DIR)
    extract_sales_accounts(ALL_ACCOUNTS_VIEW_ID, OUTPUT_DIR)
    extract_data("deals", ALL_DEALS_VIEW_ID, OUTPUT_DIR)

    # Ingest and Transform Data Phase
    print("Transforming data...")
    contacts_data, deals_data, accounts_data, accounts_contacts_data = load_data_from_files(OUTPUT_DIR)
    contacts_df, deals_df, accounts_df, accounts_contacts_df, companies_df = transform_data(contacts_data, deals_data, accounts_data, accounts_contacts_data)
    contacts_df.to_csv("contacts.csv", index=False)
    deals_df.to_csv("deals.csv", index=False)
    accounts_df.to_csv("accounts.csv", index=False)
    accounts_contacts_df.to_csv("accounts_contacts.csv", index=False)
    companies_df.to_csv("companies.csv", index=False)
    print(companies_df)

    # Load into PostgreSQL
    print("Loading data to PostgreSQL...")
    DB_NAME = os.getenv("POSTGRES_DB", "crm_db")
    DB_USER = os.getenv("POSTGRES_USER", "crm_user")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
    DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
    DB_PORT = os.getenv("POSTGRES_PORT", "5432")

    CONN_STRING = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    engine = sqlalchemy.create_engine(CONN_STRING)

    load_dataframe_to_postgres(contacts_df, "contacts", engine)
    load_dataframe_to_postgres(deals_df, "deals", engine)
    load_dataframe_to_postgres(accounts_df, "accounts", engine)
    load_dataframe_to_postgres(companies_df, "contact_deal", engine)

    # Aggregation Phase
    print("Calculating aggregated data...")
    aggregate_deals_per_contact(engine)
    aggregated_contacts_per_account(engine)
    contacts_list(companies_df) 

    print("Data pipeline completed successfully.")