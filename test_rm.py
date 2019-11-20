
import pandas as pd
import unittest

from rightmove_webscraper import RightmoveData


base_url = "https://www.rightmove.co.uk/"
columns = sorted(["price", "type", "address", "url", "agent_url", "postcode", "number_bedrooms", "search_date"])


class RightmoveWebscraperTest(unittest.TestCase):
    """Unit tests for the `RightmoveWebscraper` class."""

    def test_sale(self):
        """Test a search on properties for sale."""
        url = f"{base_url}property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E94346&insId=1"
        rmd = RightmoveData(url)
        self.assertIsInstance(rmd.average_price, float)
        self.assertIsInstance(rmd.get_results, pd.DataFrame)
        self.assertListEqual(sorted(rmd.get_results.columns), columns)
        self.assertGreater(len(rmd.get_results), 0)
        self.assertIsInstance(rmd.page_count, int)
        self.assertEqual(rmd.rent_or_sale, "sale")
        self.assertIsInstance(rmd.results_count, int)
        self.assertIsInstance(rmd.results_count_display, int)
        self.assertEqual(url, rmd.url)
        df = rmd.summary()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertListEqual(sorted(["number_bedrooms", "count", "mean"]), sorted(df.columns))
        self.assertGreater(len(df), 0)
        for c in columns:
            df = rmd.summary(by=c)
            self.assertIsInstance(df, pd.DataFrame)
            self.assertListEqual(sorted([c, "count", "mean"]), sorted(df.columns))
            self.assertGreater(len(df), 0)

    def test_rent(self):
        """Test a search on properties for sale."""
        url = f"{base_url}property-to-rent/find.html?searchType=RENT&locationIdentifier=REGION%5E94346"
        rmd = RightmoveData(url)
        self.assertIsInstance(rmd.average_price, float)
        self.assertIsInstance(rmd.get_results, pd.DataFrame)
        self.assertListEqual(sorted(rmd.get_results.columns), columns)
        self.assertGreater(len(rmd.get_results), 0)
        self.assertIsInstance(rmd.page_count, int)
        self.assertEqual(rmd.rent_or_sale, "rent")
        self.assertIsInstance(rmd.results_count, int)
        self.assertIsInstance(rmd.results_count_display, int)
        self.assertEqual(url, rmd.url)
        df = rmd.summary()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertListEqual(sorted(["number_bedrooms", "count", "mean"]), sorted(df.columns))
        self.assertGreater(len(df), 0)
        for c in columns:
            df = rmd.summary(by=c)
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
