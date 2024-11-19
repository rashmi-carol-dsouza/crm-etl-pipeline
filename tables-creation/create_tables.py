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
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    zipcode VARCHAR(20),
    country VARCHAR(100),
    number_of_employees INTEGER,
    annual_revenue DECIMAL,
    website VARCHAR(255),
    phone VARCHAR(50),
    open_deals_amount DECIMAL,
    open_deals_count INTEGER,
    won_deals_amount DECIMAL,
    won_deals_count INTEGER,
    industry VARCHAR(255),
    region VARCHAR(100),
    account_value DECIMAL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    last_assigned_at TIMESTAMP,
    custom_field JSONB,
    tags VARCHAR(255),
    team_user_ids VARCHAR(255),
    domains VARCHAR(255)
);
"""

create_contacts_table = """
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES accounts(id),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    display_name VARCHAR(255),
    job_title VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    email VARCHAR(255),
    mobile_number VARCHAR(50),
    phone_numbers VARCHAR(255),
    lead_score INTEGER,
    open_deals_amount DECIMAL,
    won_deals_amount DECIMAL,
    lead_source VARCHAR(255),
    last_contacted_date TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    last_assigned_at TIMESTAMP,
    custom_field JSONB,
    tags VARCHAR(255),
    team_user_ids VARCHAR(255),
    subscription_status VARCHAR(100)
);
"""

create_deals_table = """
CREATE TABLE IF NOT EXISTS deals (
    id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES accounts(id),
    name VARCHAR(255) NOT NULL,
    amount DECIMAL,
    base_currency_amount DECIMAL,
    deal_size DECIMAL,
    probability_of_closure DECIMAL,
    deal_stage VARCHAR(255),
    expected_close TIMESTAMP,
    closed_date TIMESTAMP,
    deal_pipeline_id VARCHAR(100),
    deal_stage_id VARCHAR(100),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    last_assigned_at TIMESTAMP,
    deal_prediction JSONB,
    deal_price_adjustments JSONB,
    tags VARCHAR(255)
);
"""

create_aggregated_metrics_table = """
CREATE TABLE IF NOT EXISTS aggregated_metrics (
    account_id INTEGER REFERENCES accounts(id),
    aggregation_type VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    total_contacts INTEGER,
    total_deals_amount DECIMAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (account_id, aggregation_type, date)
);
"""

# Execute the SQL commands to create tables
cur.execute(create_accounts_table)
cur.execute(create_contacts_table)
cur.execute(create_deals_table)
cur.execute(create_aggregated_metrics_table)

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()

print("Tables created successfully in PostgreSQL database.")
