
import pandas as pd
import unittest

from rightmove_webscraper import RightmoveData


base_url = "https://www.rightmove.co.uk/"
columns = sorted(["price", "type", "address", "url", "agent_url", "postcode", "number_bedrooms", "search_date"])


class RightmoveDataTest(unittest.TestCase):
    """Unit tests for the `RightmoveData` class."""

    def test_sale_residential(self):
        """Test a search on residential properties for sale."""
        url = f"{base_url}property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E94346&insId=1"
        rm = RightmoveData(url)
        self.assertIsInstance(rm.average_price, float)
        self.assertIsInstance(rm.get_results, pd.DataFrame)
        self.assertListEqual(sorted(rm.get_results.columns), columns)
        self.assertGreater(len(rm.get_results), 0)
        self.assertIsInstance(rm.page_count, int)
        self.assertEqual(rm.rent_or_sale, "sale")
        self.assertIsInstance(rm.results_count, int)
        self.assertIsInstance(rm.results_count_display, int)
        self.assertEqual(url, rm.url)
        df = rm.summary()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertListEqual(sorted(["number_bedrooms", "count", "mean"]), sorted(df.columns))
        self.assertGreater(len(df), 0)
        for c in columns:
            df = rm.summary(by=c)
            self.assertIsInstance(df, pd.DataFrame)
            self.assertListEqual(sorted([c, "count", "mean"]), sorted(df.columns))
            self.assertGreater(len(df), 0)

    def test_rent_residential(self):
        """Test a search on residential properties for rent."""
        url = f"{base_url}property-to-rent/find.html?searchType=RENT&locationIdentifier=REGION%5E94346"
        rm = RightmoveData(url)
        self.assertIsInstance(rm.average_price, float)
        self.assertIsInstance(rm.get_results, pd.DataFrame)
        self.assertListEqual(sorted(rm.get_results.columns), columns)
        self.assertGreater(len(rm.get_results), 0)
        self.assertIsInstance(rm.page_count, int)
        self.assertEqual(rm.rent_or_sale, "rent")
        self.assertIsInstance(rm.results_count, int)
        self.assertIsInstance(rm.results_count_display, int)
        self.assertEqual(url, rm.url)
        df = rm.summary()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertListEqual(sorted(["number_bedrooms", "count", "mean"]), sorted(df.columns))
        self.assertGreater(len(df), 0)
        for c in columns:
            df = rm.summary(by=c)
            self.assertIsInstance(df, pd.DataFrame)
            self.assertListEqual(sorted([c, "count", "mean"]), sorted(df.columns))
            self.assertGreater(len(df), 0)

    def test_sale_commercial(self):
        """Test a search on commercial properties for sale."""
        url = f"{base_url}commercial-property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E70417"
        rm = RightmoveData(url)
        self.assertIsInstance(rm.average_price, float)
        self.assertIsInstance(rm.get_results, pd.DataFrame)
        self.assertListEqual(sorted(rm.get_results.columns), columns)
        self.assertGreater(len(rm.get_results), 0)
        self.assertIsInstance(rm.page_count, int)
        self.assertEqual(rm.rent_or_sale, "sale-commercial")
        self.assertIsInstance(rm.results_count, int)
        self.assertIsInstance(rm.results_count_display, int)
        self.assertEqual(url, rm.url)
        df = rm.summary()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertListEqual(sorted(["type", "count", "mean"]), sorted(df.columns))
        self.assertGreater(len(df), 0)
        for c in columns:
            if c == "number_bedrooms":
                continue
            df = rm.summary(by=c)
            self.assertIsInstance(df, pd.DataFrame)
            self.assertListEqual(sorted([c, "count", "mean"]), sorted(df.columns))
            self.assertGreater(len(df), 0)

    def test_rent_commercial(self):
        """Test a search on commercial properties for rent."""
        url = f"{base_url}commercial-property-to-let/find.html?searchType=RENT&locationIdentifier=REGION%5E70417"
        rm = RightmoveData(url)
        self.assertIsInstance(rm.average_price, float)
        self.assertIsInstance(rm.get_results, pd.DataFrame)
        self.assertListEqual(sorted(rm.get_results.columns), columns)
        self.assertGreater(len(rm.get_results), 0)
        self.assertIsInstance(rm.page_count, int)
        self.assertEqual(rm.rent_or_sale, "rent-commercial")
        self.assertIsInstance(rm.results_count, int)
        self.assertIsInstance(rm.results_count_display, int)
        self.assertEqual(url, rm.url)
        df = rm.summary()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertListEqual(sorted(["type", "count", "mean"]), sorted(df.columns))
        self.assertGreater(len(df), 0)
        for c in columns:
            if c == "number_bedrooms":
                continue
            df = rm.summary(by=c)
            self.assertIsInstance(df, pd.DataFrame)
            self.assertListEqual(sorted([c, "count", "mean"]), sorted(df.columns))
            self.assertGreater(len(df), 0)

    def test_bad_url(self):
        """Test a bad URL raises a value error."""
        bad_url = "https://www.rightmove.co.uk/property"
        with self.assertRaises(ValueError):
            _ = RightmoveData(bad_url)


if __name__ == "__main__":
    unittest.main()
