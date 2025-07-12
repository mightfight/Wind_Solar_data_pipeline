import requests
import pandas as pd
import sqlite3
from time import sleep
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Constants
DB_NAME = "generation_data.db"
TABLE_NAME = "wind_solar_data"
API_URL = "https://data.elexon.co.uk/bmrs/api/v1/generation/actual/per-type/wind-and-solar"

def create_db():
    """Creates the SQLite DB and the table if not already present."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                publishTime TEXT,
                businessType TEXT,
                psrType TEXT,
                quantity REAL,
                startTime TEXT,
                settlementDate TEXT,
                settlementPeriod INTEGER
            );
        """)
        conn.commit()

def fetch_weekly_data(start_date, end_date):
    """Fetches data from the API for a given week."""
    params = {
        "from": start_date.strftime("%Y-%m-%d"),
        "to": end_date.strftime("%Y-%m-%d"),
        "format": "json"
    }
    try:
        response = requests.get(API_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data.get("data", []))
    except Exception as e:
        print(f"Error fetching {start_date} to {end_date}: {e}")
        return pd.DataFrame()

def store_to_db(df):
    """Stores a DataFrame to the SQLite database."""
    if not df.empty:
        with sqlite3.connect(DB_NAME) as conn:
            df.to_sql(TABLE_NAME, conn, if_exists="append", index=False)

def fetch_yearly_data_in_batches():
    """Fetches 1 year's worth of data in weekly chunks and stores them. Wait for 0.5s between each batch"""
    end_date = datetime.now().date()
    start_date = end_date - relativedelta(years=1)
    current = start_date

    while current < end_date:
        next_week = current + relativedelta(weeks=1)
        if next_week > end_date:
            next_week = end_date
        print(f"📦 Fetching data from {current} to {next_week}...")
        df = fetch_weekly_data(current, next_week)
        store_to_db(df)
        print(f"📦 Stored data from {current} to {next_week}...")
        sleep(0.5)
        current = next_week

    print("✅ Data fetching and storing complete.")

def print_psrtype_business_combinations():
    """Prints unique combinations of psrType and businessType with their counts."""
    with sqlite3.connect(DB_NAME) as conn:
        df = pd.read_sql_query(f"SELECT businessType, psrType, count(*) FROM {TABLE_NAME} group by psrType, businessType", conn)

    # combo_counts = df.groupby(['psrType', 'businessType']).size().reset_index(name='count')
    print("\n📊 Unique (psrType, businessType) combinations:\n")
    print(df.to_string(index=False))

if __name__ == "__main__":
    create_db()
#   fetch_yearly_data_in_batches()
    print_psrtype_business_combinations()

# if __name__ == "__main__":
#     create_db()
#     fetch_yearly_data_in_batches()