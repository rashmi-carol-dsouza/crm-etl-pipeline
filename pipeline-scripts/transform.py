import pandas as pd
import json
import os

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
        accounts_data = json.load(accounts_file)

    return contacts_data, deals_data, accounts_data

def flatten_nested_columns(df, nested_columns):
    """Flatten specified nested columns in the DataFrame."""
    for column in nested_columns:
        if column in df.columns:
            nested_df = df[column].apply(pd.Series)
            df = pd.concat([df, nested_df], axis=1)
            df.drop(columns=[column], inplace=True)
    return df

# Load data to df
def load_data_to_dataframe(contacts_data, deals_data, accounts_data):
    # Convert each JSON list to a DataFrame
    contacts_df = pd.DataFrame(contacts_data)
    deals_df = pd.DataFrame(deals_data)
    accounts_df = pd.DataFrame(accounts_data)

    # Flatten nested columns
    contacts_df = flatten_nested_columns(contacts_df, ['custom_field'])
    deals_df = flatten_nested_columns(deals_df, ['custom_field'])
    accounts_df = flatten_nested_columns(accounts_df, ['links', 'custom_field'])
    return contacts_df, deals_df, accounts_df

def clean_dataframe(df):
    """
    Clean the given DataFrame by dropping empty columns, removing duplicate rows,
    and replacing NaN values.
    """
    # Drop columns that are completely empty
    df.dropna(axis=1, how='all', inplace=True)

    # Drop completely duplicated columns
    hashable_cols = df.columns[~df.applymap(lambda x: isinstance(x, (list, dict))).any()]
    df = df.loc[:, hashable_cols].T.drop_duplicates().T

    # Remove rows that are completely duplicated
    hashable_columns = [col for col in df.columns if df[col].apply(lambda x: not isinstance(x, (list, dict))).all()]
    df.drop_duplicates(subset=hashable_columns, inplace=True)

    # Replace NaN values with appropriate values for PostgreSQL
    for column in df.columns:
        if df[column].dtype in ['int64', 'float64']:
            df[column].fillna(0, inplace=True)
        elif df[column].dtype == 'object':
            df[column].fillna('Unknown', inplace=True)
        else:
            df[column].fillna('NULL', inplace=True)

    return df

# Transform data
def transform_data(contacts_data, deals_data, accounts_data):
    # Load JSON data into DataFrames
    contacts_df, deals_df, accounts_df = load_data_to_dataframe(contacts_data, deals_data, accounts_data)

    # Clean the DataFrames
    contacts_df = clean_dataframe(contacts_df)
    deals_df = clean_dataframe(deals_df)
    accounts_df = clean_dataframe(accounts_df)
    return contacts_df, deals_df, accounts_df


   