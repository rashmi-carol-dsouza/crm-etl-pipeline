import psycopg2
from psycopg2 import sql
import os

# Load environment variables for PostgreSQL connection
db_name = os.getenv("POSTGRES_DB", "crm_db")
print(db_name)
db_user = os.getenv("POSTGRES_USER", "crm_user")
db_password = os.getenv("POSTGRES_PASSWORD", "password")
db_host = os.getenv("POSTGRES_HOST", "localhost")
db_port = os.getenv("POSTGRES_PORT", "5432")

# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port
)

# Create a cursor object to execute SQL commands
cur = conn.cursor()

# SQL to create tables
create_accounts_table = """
CREATE TABLE IF NOT EXISTS accounts (
   id BIGINT PRIMARY KEY,
    address VARCHAR(255),
    annual_revenue DECIMAL(15, 2),
    appointments TEXT,
    avatar TEXT,
    cf_account_value DECIMAL(15, 2),
    cf_region VARCHAR(255),
    city VARCHAR(255),
    conversations TEXT,
    country VARCHAR(255),
    created_at TIMESTAMP,
    document_associations TEXT,
    facebook VARCHAR(255),
    is_deleted BOOLEAN,
    last_assigned_at TIMESTAMP,
    linkedin VARCHAR(255),
    name VARCHAR(255),
    notes TEXT,
    number_of_employees INTEGER,
    open_deals_amount DECIMAL(15, 2),
    open_deals_count INTEGER,
    owner_id BIGINT,
    phone VARCHAR(255),
    record_type_id BIGINT,
    state VARCHAR(255),
    tasks TEXT,
    twitter VARCHAR(255),
    updated_at TIMESTAMP,
    website VARCHAR(255),
    won_deals_amount DECIMAL(15, 2),
    won_deals_count INTEGER,
    zipcode VARCHAR(255)
);
"""

create_contacts_table = """
CREATE TABLE IF NOT EXISTS contacts (
avatar TEXT,
    cf_last_contacted_date TIMESTAMP,
    cf_lead_source VARCHAR(255),
    city VARCHAR(255),
    country VARCHAR(255),
    created_at TIMESTAMP,
    customer_fit VARCHAR(255),
    display_name VARCHAR(255),
    email VARCHAR(255),
    first_name VARCHAR(255),
    id BIGINT PRIMARY KEY,
    is_deleted BOOLEAN,
    job_title VARCHAR(255),
    last_assigned_at TIMESTAMP,
    last_name VARCHAR(255),
    lead_score INTEGER,
    linkedin VARCHAR(255),
    mcr_id VARCHAR(255),
    mobile_number VARCHAR(255),
    open_deals_amount DECIMAL(15, 2),
    open_deals_count INTEGER,
    record_type_id BIGINT,
    sms_subscription_status VARCHAR(255),
    state VARCHAR(255),
    subscription_status VARCHAR(255),
    subscription_types VARCHAR(255),
    time_zone VARCHAR(255),
    updated_at TIMESTAMP,
    won_deals_amount DECIMAL(15, 2),
    won_deals_count INTEGER
);
"""

create_deals_table = """
CREATE TABLE IF NOT EXISTS deals (
    id BIGINT PRIMARY KEY,
    age INTEGER,
    amount DECIMAL(15, 2),
    cf_deal_size VARCHAR(255),
    cf_deal_stage VARCHAR(255),
    cf_probability_of_closure DECIMAL(15, 2),
    closed_date TIMESTAMP,
    created_at TIMESTAMP,
    deal_pipeline_id BIGINT,
    deal_prediction VARCHAR(255),
    deal_prediction_last_updated_at TIMESTAMP,
    deal_stage_id BIGINT,
    expected_close TIMESTAMP,
    expected_deal_value DECIMAL(15, 2),
    forecast_category VARCHAR(255),
    has_products BOOLEAN,
    last_assigned_at TIMESTAMP,
    name VARCHAR(255),
    probability DECIMAL(15, 2),
    record_type_id BIGINT,
    updated_at TIMESTAMP,
    sales_account_id BIGINT,
    FOREIGN KEY (sales_account_id) REFERENCES accounts(id)
);
"""

create_contact_deal_table = """
CREATE TABLE IF NOT EXISTS contact_deal (
    contact_id BIGINT PRIMARY KEY,
    sales_account_id BIGINT,
    FOREIGN KEY (sales_account_id) REFERENCES accounts(id)
);
"""

# Execute the SQL commands to create tables
cur.execute(create_accounts_table)
cur.execute(create_contacts_table)
cur.execute(create_deals_table)
cur.execute(create_contact_deal_table)

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()

print("Tables created successfully in PostgreSQL database.")
