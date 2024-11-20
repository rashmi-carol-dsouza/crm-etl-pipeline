import pandas as pd
import json
import os

pd.set_option('future.no_silent_downcasting', True)

# Load data from JSON files
def load_data_from_files(data_folder):
    contacts_data_path = os.path.join(data_folder, 'contacts.json')
    deals_data_path = os.path.join(data_folder, 'deals.json')
    accounts_data_path = os.path.join(data_folder, 'sales_accounts.json')

    with open(contacts_data_path) as contacts_file:
        contacts_data = json.load(contacts_file)
    with open(deals_data_path) as deals_file:
        deals_data = json.load(deals_file)
    with open(accounts_data_path) as accounts_file:
        accounts_raw_data = json.load(accounts_file)
        accounts_data = accounts_raw_data['sales_accounts']
        accounts_contacts_data = accounts_raw_data['contacts']

    return contacts_data, deals_data, accounts_data, accounts_contacts_data

def flatten_nested_columns(df, nested_columns):
    """Flatten specified nested columns in the DataFrame."""
    for column in nested_columns:
        if column in df.columns:
            nested_df = df[column].apply(pd.Series)
            df = pd.concat([df, nested_df], axis=1)
            df.drop(columns=[column], inplace=True)
    return df

# Load data to df
def load_data_to_dataframe(contacts_data, deals_data, accounts_data, accounts_contacts_data):
    # Convert each JSON list to a DataFrame
    contacts_df = pd.DataFrame(contacts_data)
    deals_df = pd.DataFrame(deals_data)
    accounts_df = pd.DataFrame(accounts_data)
    accounts_contacts_df = pd.DataFrame(accounts_contacts_data)

    data = []

    # Iterate through each row in the accounts_df
    for _, row in accounts_df.iterrows():
        account_id = row['id']
        contact_ids = row['contact_ids']
        
        # Iterate through each contact_id in the contact_ids list
        if isinstance(contact_ids, list):  # Ensure contact_ids is a list
            for contact_id in contact_ids:
                # Append a dictionary to the data list
                data.append({'contact_id': contact_id, 'sales_account_id': account_id})

    # Create a new DataFrame from the data list
    companies_df = pd.DataFrame(data)

    # Flatten nested columns
    contacts_df = flatten_nested_columns(contacts_df, ['custom_field'])
    deals_df = flatten_nested_columns(deals_df, ['custom_field'])
    accounts_df = flatten_nested_columns(accounts_df, ['links', 'custom_field'])
    
    return contacts_df, deals_df, accounts_df, accounts_contacts_df, companies_df



def clean_dataframe(df, entity):
    """
    Clean the given DataFrame by keeping only the specified columns for contacts, accounts, and deals.
    """
    # Define the columns to keep for each type of entity
    columns_to_keep = {
        'contacts': [
            'avatar', 'cf_last_contacted_date', 'cf_lead_source', 'city', 'country', 'created_at', 'customer_fit',
            'display_name', 'email', 'first_name', 'id', 'is_deleted', 'job_title', 'last_assigned_at', 'last_name',
            'lead_score', 'linkedin', 'mcr_id', 'mobile_number', 'open_deals_amount', 'open_deals_count',
            'record_type_id', 'sms_subscription_status', 'state', 'subscription_status', 'subscription_types',
            'time_zone', 'updated_at', 'won_deals_amount', 'won_deals_count'
        ],
        'accounts': [
            'address', 'annual_revenue', 'appointments', 'avatar', 'cf_account_value', 'cf_region', 'city',
            'conversations', 'country', 'created_at', 'document_associations', 'facebook', 'id', 'is_deleted',
            'last_assigned_at', 'linkedin', 'name', 'notes', 'number_of_employees', 'open_deals_amount',
            'open_deals_count', 'owner_id', 'phone', 'record_type_id', 'state', 'tasks', 'twitter', 'updated_at',
            'website', 'won_deals_amount', 'won_deals_count', 'zipcode'
        ],
        'deals': [
            'age', 'amount', 'cf_deal_size', 'cf_deal_stage', 'cf_probability_of_closure', 'closed_date', 'created_at',
            'deal_pipeline_id', 'deal_prediction', 'deal_prediction_last_updated_at', 'deal_stage_id', 'expected_close',
            'expected_deal_value', 'forecast_category', 'has_products', 'id', 'last_assigned_at', 'name', 'probability',
            'record_type_id', 'updated_at', "sales_account_id"
        ]
    }

    # Get the columns to keep for the current entity
    keep_columns = columns_to_keep.get(entity, [])

    # Keep only the specified columns and drop others
    df = df[keep_columns]

    # Remove rows that are completely duplicated, considering only hashable columns
    hashable_columns = [col for col in df.columns if df[col].apply(lambda x: not isinstance(x, (list, dict))).all()]
    df.drop_duplicates(subset=hashable_columns)

    # Replace NaN values with appropriate values
    for column in df.columns:
        if df[column].dtype in ['int64', 'float64']:
            df.loc[:, column] = df[column].fillna(0)  # Using .loc to avoid SettingWithCopyWarning
        elif df[column].dtype == 'object':
            pass
        else:
            df.loc[:, column] = df[column].fillna('NULL')

    return df


# Transform data
def transform_data(contacts_data, deals_data, accounts_data, accounts_contacts_data):
    # Load JSON data into DataFrames
    contacts_df, deals_df, accounts_df, accounts_contacts_df, companies_df = load_data_to_dataframe(contacts_data, deals_data, accounts_data, accounts_contacts_data)

    # Clean the DataFrames
    contacts_df = clean_dataframe(contacts_df,"contacts")
    deals_df = clean_dataframe(deals_df,"deals")
    accounts_df = clean_dataframe(accounts_df,"accounts")
    return contacts_df, deals_df, accounts_df, accounts_contacts_df, companies_df


   


   