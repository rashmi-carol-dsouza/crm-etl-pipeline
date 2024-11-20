from sqlalchemy import text

def aggregate_deals_per_contact(engine):
    with engine.connect() as connection:
        aggregate_query = text("""
        CREATE TABLE IF NOT EXISTS aggregated_deals_per_contact AS
        WITH deals_with_accounts AS (
            SELECT
                d.sales_account_id,
                d.amount,
                d.created_at
            FROM deals d
            WHERE d.sales_account_id IS NOT NULL
        ),
        daily_aggregates AS (
            SELECT 
                sales_account_id,
                DATE_TRUNC('day', created_at) AS period,
                SUM(amount) AS daily_total_amount
            FROM deals_with_accounts
            GROUP BY sales_account_id, period
        ),
        weekly_aggregates AS (
            SELECT 
                sales_account_id,
                DATE_TRUNC('week', created_at) AS period,
                SUM(amount) AS weekly_total_amount
            FROM deals_with_accounts
            GROUP BY sales_account_id, period
        ),
        monthly_aggregates AS (
            SELECT 
                sales_account_id,
                DATE_TRUNC('month', created_at) AS period,
                SUM(amount) AS monthly_total_amount
            FROM deals_with_accounts
            GROUP BY sales_account_id, period
        )
        SELECT 
            COALESCE(daily.sales_account_id, weekly.sales_account_id, monthly.sales_account_id) AS sales_account_id,
            COALESCE(daily.period, weekly.period, monthly.period) AS created_at,
            COALESCE(daily.daily_total_amount, 0) AS daily_total_amount,
            COALESCE(weekly.weekly_total_amount, 0) AS weekly_total_amount,
            COALESCE(monthly.monthly_total_amount, 0) AS monthly_total_amount
        FROM daily_aggregates daily
        FULL OUTER JOIN weekly_aggregates weekly
            ON daily.sales_account_id = weekly.sales_account_id AND daily.period = weekly.period
        FULL OUTER JOIN monthly_aggregates monthly
            ON daily.sales_account_id = monthly.sales_account_id AND daily.period = monthly.period;
        """)
        connection.execute(aggregate_query)


def aggregated_contacts_per_account(engine):
    with engine.connect() as connection:
        aggregate_query = text("""
        CREATE TABLE IF NOT EXISTS aggregated_contacts_per_account AS
        WITH contacts_with_accounts AS (
            SELECT 
                cd.sales_account_id,
                c.created_at,
                cd.contact_id
            FROM 
                contact_deal cd
            JOIN 
                contacts c 
            ON 
                cd.contact_id = c.id
            WHERE 
                cd.sales_account_id IS NOT NULL
        ),
        daily_aggregates AS (
            SELECT
                sales_account_id,
                DATE_TRUNC('day', created_at) AS period,
                COUNT(DISTINCT contact_id) AS daily_total_contacts
            FROM 
                contacts_with_accounts
            GROUP BY 
                sales_account_id, period
        ),
        weekly_aggregates AS (
            SELECT
                sales_account_id,
                DATE_TRUNC('week', created_at) AS period,
                COUNT(DISTINCT contact_id) AS weekly_total_contacts
            FROM 
                contacts_with_accounts
            GROUP BY 
                sales_account_id, period
        ),
        monthly_aggregates AS (
            SELECT
                sales_account_id,
                DATE_TRUNC('month', created_at) AS period,
                COUNT(DISTINCT contact_id) AS monthly_total_contacts
            FROM 
                contacts_with_accounts
            GROUP BY 
                sales_account_id, period
        )
        SELECT
            COALESCE(daily.sales_account_id, weekly.sales_account_id, monthly.sales_account_id) AS sales_account_id,
            COALESCE(daily.period, weekly.period, monthly.period) AS created_at,
            COALESCE(daily.daily_total_contacts, 0) AS daily_total_contacts,
            COALESCE(weekly.weekly_total_contacts, 0) AS weekly_total_contacts,
            COALESCE(monthly.monthly_total_contacts, 0) AS monthly_total_contacts
        FROM 
            daily_aggregates daily
        FULL OUTER JOIN 
            weekly_aggregates weekly
            ON daily.sales_account_id = weekly.sales_account_id AND daily.period = weekly.period
        FULL OUTER JOIN 
            monthly_aggregates monthly
            ON COALESCE(daily.sales_account_id, weekly.sales_account_id) = monthly.sales_account_id 
            AND COALESCE(daily.period, weekly.period) = monthly.period;
        """)
        connection.execute(aggregate_query)
    
def contacts_list(df):
    grouped_contacts = df.groupby('sales_account_id')['contact_id'].apply(list).reset_index()
    output_file = 'data/contacts_per_account.txt'

    with open(output_file, 'w') as f:
        for _, row in grouped_contacts.iterrows():
            sales_account_id = row['sales_account_id']
            customer_ids = row['contact_id']
            f.write(f'Sales Account ID: {sales_account_id}\n')
            f.write('Contacts:\n')
            for customer_id in customer_ids:
                f.write(f'  - {customer_id}\n')
            f.write('\n')
    print(f"Contacts per account written to {output_file}")
