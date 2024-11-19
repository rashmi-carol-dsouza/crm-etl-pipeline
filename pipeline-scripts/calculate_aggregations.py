import pandas as pd

def calculate_aggregates(deals_df, contacts_df, accounts_df):
    """
    Calculate daily, weekly, and monthly aggregates for deals and contacts.

    Args:
        deals_df (DataFrame): Deals DataFrame containing 'created_at', 'amount', and 'record_type_id'.
        contacts_df (DataFrame): Contacts DataFrame containing 'created_at' and 'record_type_id'.
        accounts_df (DataFrame): Accounts DataFrame containing 'id' as 'account_id'.

    Returns:
        dict: Dictionary containing the aggregated DataFrames.
    """
    # Ensure 'created_at' is in datetime format for both deals and contacts
    deals_df['created_at'] = pd.to_datetime(deals_df['created_at'], errors='coerce')
    contacts_df['created_at'] = pd.to_datetime(contacts_df['created_at'], errors='coerce')

    # Drop rows with invalid dates in 'created_at'
    deals_df.dropna(subset=['created_at'], inplace=True)
    contacts_df.dropna(subset=['created_at'], inplace=True)

    # Ensure that 'record_type_id' and 'id' are of the same data type (convert to string)
    deals_df['record_type_id'] = deals_df['record_type_id'].astype(str)
    accounts_df['id'] = accounts_df['id'].astype(str)

    # Merge deals with accounts to include 'account_id' column
    merged_deals = deals_df.merge(accounts_df[['id']], how='left', left_on='record_type_id', right_on='id')
    
    # Rename 'id_y' column from accounts to 'account_id'
    if 'id_y' in merged_deals.columns:
        merged_deals.rename(columns={'id_y': 'account_id'}, inplace=True)
    else:
        print("Warning: 'id_y' column not found in merged_deals after merge operation.")

    # Print columns after renaming for debugging
    print("Merged Deals Columns after renaming:", merged_deals.columns)

    # Check if 'account_id' is present
    if 'account_id' not in merged_deals.columns:
        print("Error: 'account_id' column is missing from merged_deals.")
        return None

    # Drop rows where 'account_id' is NaN after the merge
    merged_deals.dropna(subset=['account_id'], inplace=True)

    # Convert 'account_id' to string to avoid issues with aggregation
    merged_deals['account_id'] = merged_deals['account_id'].astype(str)

    # Compute deals daily, weekly, and monthly aggregates
    deals_daily_agg = merged_deals.groupby(['account_id', pd.Grouper(key='created_at', freq='D')])['amount'].sum().reset_index()
    deals_weekly_agg = merged_deals.groupby(['account_id', pd.Grouper(key='created_at', freq='W')])['amount'].sum().reset_index()
    deals_monthly_agg = merged_deals.groupby(['account_id', pd.Grouper(key='created_at', freq='M')])['amount'].sum().reset_index()

    # Ensure 'record_type_id' is of the same type in contacts_df and accounts_df
    contacts_df['record_type_id'] = contacts_df['record_type_id'].astype(str)

    # Compute contacts daily, weekly, and monthly aggregates
    contacts_daily_agg = contacts_df.groupby(['record_type_id', pd.Grouper(key='created_at', freq='D')]).size().reset_index(name='total_contacts')
    contacts_weekly_agg = contacts_df.groupby(['record_type_id', pd.Grouper(key='created_at', freq='W')]).size().reset_index(name='total_contacts')
    contacts_monthly_agg = contacts_df.groupby(['record_type_id', pd.Grouper(key='created_at', freq='M')]).size().reset_index(name='total_contacts')

    return {
        'deals_daily_agg': deals_daily_agg,
        'deals_weekly_agg': deals_weekly_agg,
        'deals_monthly_agg': deals_monthly_agg,
        'contacts_daily_agg': contacts_daily_agg,
        'contacts_weekly_agg': contacts_weekly_agg,
        'contacts_monthly_agg': contacts_monthly_agg
    }

def generate_contacts_per_account(contacts_df):
    """
    Generate a list of contacts for each account.

    Args:
        contacts_df (DataFrame): Contacts DataFrame containing 'record_type_id' and 'display_name'.

    Returns:
        DataFrame: DataFrame with 'record_type_id' and a list of 'contacts'.
    """
    # Group contacts by 'record_type_id' and create a list of 'display_name' for each account
    contacts_per_account = contacts_df.groupby('record_type_id')['display_name'].apply(list).reset_index(name='contacts')
    
    return contacts_per_account
