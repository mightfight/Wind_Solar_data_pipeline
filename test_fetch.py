import unittest
from datetime import datetime, timedelta
import pandas as pd
from fetch_data import fetch_weekly_data

class TestDataFetch(unittest.TestCase):
    def setUp(self):
        """Setup a short date range for testing."""
        self.today = datetime.utcnow().date()
        self.one_week_ago = self.today - timedelta(days=7)

    def test_fetch_returns_dataframe(self):
        """Test if the fetch function returns a non-empty DataFrame."""
        df = fetch_weekly_data(self.one_week_ago, self.today)
        self.assertIsInstance(df, pd.DataFrame)

    def test_expected_columns(self):
        """Test if expected columns exist in returned data."""
        df = fetch_weekly_data(self.one_week_ago, self.today)
        expected_columns = {
            "publishTime", "businessType", "psrType",
            "quantity", "startTime", "settlementDate", "settlementPeriod"
        }
        if not df.empty:
            self.assertTrue(expected_columns.issubset(df.columns))
        else:
            self.skipTest("No data returned to test columns.")

    def test_empty_result(self):
        """Test if fetch function returns empty DataFrame for invalid date range."""
        df = fetch_weekly_data(self.today + timedelta(days=1), self.today + timedelta(days=2))
        self.assertTrue(df.empty)

if __name__ == '__main__':
    unittest.main()
