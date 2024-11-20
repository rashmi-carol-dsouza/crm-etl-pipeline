import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import os
import requests
import json
from dotenv import load_dotenv


load_dotenv()

# Update for database

DB_NAME = os.getenv("POSTGRES_DB", "crm_db")
DB_USER = os.getenv("POSTGRES_USER", "crm_user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

CONN_STRING = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(CONN_STRING)

def update_deal_in_db(deal_id, new_deal_size):
    try:
        with engine.connect() as connection:
            update_query = text("""
            UPDATE deals
            SET cf_deal_size = :new_deal_size
            WHERE id = :deal_id;
            """)
            connection.execute(update_query, {'deal_id': deal_id, 'new_deal_size': new_deal_size})
            print(f"Updated deal id {deal_id} in PostgreSQL with cf_deal_size to {new_deal_size}.")
    except SQLAlchemyError as e:
        print(f"Error while updating deal id {deal_id} in PostgreSQL: {str(e)}")

update_deal_in_db(202000322319, 24456)

#Update for freshworks


FRESHSALES_API_KEY = os.getenv('FRESHSALES_API_KEY')
SALES_BUNDLE_ALIAS = os.getenv('SALES_BUNDLE_ALIAS')

if not FRESHSALES_API_KEY or not SALES_BUNDLE_ALIAS:
    raise ValueError("FRESHSALES_API_KEY or SALES_BUNDLE_ALIAS environment variable is missing.")

def upsert_deal(deal_id, deal_size):
    url = f"https://{SALES_BUNDLE_ALIAS}/api/deals/upsert"

    headers = {
        "Authorization": f"Token token={FRESHSALES_API_KEY}",
        "Content-Type": "application/json"
    }


    payload = {
        "unique_identifier": {
            "id": str(deal_id)  
        },
        "deal": {
            "custom_field": {
                "cf_deal_size": str(deal_size)  
            }
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        print(f"Successfully updated deal id {deal_id} in Freshworks to deal size {deal_size}.")
    elif response.status_code == 201:
        print(f"Successfully created a new deal with id {deal_id} and deal size {deal_size}.")
    else:
        print(f"Failed to update deal id {deal_id}. Status Code: {response.status_code}")
        print(f"Response Content: {response.content.decode()}")

if __name__ == "__main__":
    deal_id = 202000322319
    new_deal_size = 24456

    upsert_deal(deal_id, new_deal_size)