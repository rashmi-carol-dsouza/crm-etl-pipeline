import psycopg2
from sqlalchemy.exc import IntegrityError
import traceback

def load_dataframe_to_postgres(df, table_name, engine):
    try:
        df.to_sql(table_name, con=engine, if_exists='append', index=False, method='multi', chunksize=1000)
        print(f"Data successfully loaded to {table_name}")
    except IntegrityError as e:
        # Check if the exception is due to a UniqueViolation
        if isinstance(e.orig, psycopg2.errors.UniqueViolation):
            pass
        else:
            print(f"Integrity error while loading data into {table_name}: {e.__cause__}")
    except Exception as e:
        print(f"Error while loading data into {table_name}: {e.__cause__}")
        traceback.print_tb(e.__traceback__)