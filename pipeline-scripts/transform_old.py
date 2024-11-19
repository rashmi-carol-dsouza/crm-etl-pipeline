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
        accounts_data = json.load(accounts_file)

    return contacts_data, deals_data, accounts_data

def flatten_nested_columns(df, nested_columns):
    for column in nested_columns:
        if column in df.columns:
            nested_df = df[column].apply(lambda x: pd.Series(x) if isinstance(x, dict) else None)
            df = pd.concat([df, nested_df], axis=1)
            df.drop(columns=[column], inplace=True)
    return df

def ensure_created_at_column(df):
    """Ensure that the 'created_at' column exists and is in the correct format."""
    if 'created_at' not in df.columns:
        print("Warning: 'created_at' column is missing. Adding default timestamps.")
        df['created_at'] = pd.to_datetime(datetime.now())  # Add a default value if missing
    else:
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')  # Ensure proper datetime conversion
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
    # Keep a list of critical columns that should not be dropped
    critical_columns = ['created_at', 'updated_at', 'account_id']

    non_empty_cols = df.dropna(axis=1, how='all').columns
    cols_to_keep = [col for col in critical_columns if col in df.columns]
    df = df.loc[:, non_empty_cols.union(cols_to_keep)]

    # Drop completely duplicated columns, excluding critical columns
    hashable_cols = df.columns[~df.apply(lambda col: col.apply(lambda x: isinstance(x, (list, dict))).any())]
    df_before_dropping = df.copy()
    df = df.loc[:, hashable_cols.union(cols_to_keep)].T.drop_duplicates().T
    removed_cols = set(df_before_dropping.columns) - set(df.columns)


    # Remove rows that are completely duplicated, considering only hashable columns
    hashable_columns = [col for col in df.columns if df[col].apply(lambda x: not isinstance(x, (list, dict))).all()]
    df.drop_duplicates(subset=hashable_columns, inplace=True)

    # Replace NaN values with appropriate values
    for column in df.columns:
        if df[column].dtype in ['int64', 'float64']:
            df[column] = df[column].fillna(0)
        elif df[column].dtype == 'object':
            df[column] = df[column].fillna('Unknown').infer_objects(copy=False)
        else:
            df[column] = df[column].fillna('NULL')

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



   