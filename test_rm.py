
import pandas as pd
import pytest

from rightmove_webscraper import RightmoveData


base_url = "https://www.rightmove.co.uk/"
required_columns = {"address", "agent_url", "number_bedrooms", "postcode", "price", "search_date", "type", "url"}


def test_sale_residential():
    """Test a search on residential properties for sale."""
    url = f"{base_url}property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E94346&insId=1"
    rm = RightmoveData(url)
    assert isinstance(rm.average_price, float)
    assert isinstance(rm.get_results, pd.DataFrame)
    assert required_columns.issubset(set(rm.get_results.columns))
    assert len(rm.get_results) > 0
    assert isinstance(rm.page_count, int)
    assert rm.is_commercial == False
    assert isinstance(rm.results_count, int)
    assert isinstance(rm.results_count_display, int)
    assert url == rm.url
    df = rm.summary()
    assert isinstance(df, pd.DataFrame)
    assert {"number_bedrooms", "count", "mean"}.issubset(set(df.columns))
    assert len(df) > 0
    for c in required_columns:
        df = rm.summary(by=c)
        assert isinstance(df, pd.DataFrame)
        assert {c, "count", "mean"}.issubset(set(df.columns))
        assert len(df) > 0


def test_rent_residential():
    """Test a search on residential properties for rent."""
    url = f"{base_url}property-to-rent/find.html?searchType=RENT&locationIdentifier=REGION%5E94346"
    rm = RightmoveData(url)
    assert isinstance(rm.average_price, float)
    assert isinstance(rm.get_results, pd.DataFrame)
    assert required_columns.issubset(set(rm.get_results.columns))
    assert len(rm.get_results) > 0
    assert isinstance(rm.page_count, int)
    assert rm.is_commercial == False
    assert isinstance(rm.results_count, int)
    assert isinstance(rm.results_count_display, int)
    assert url == rm.url
    df = rm.summary()
    assert isinstance(df, pd.DataFrame)
    assert {"number_bedrooms", "count", "mean"}.issubset(set(df.columns))
    assert len(df) > 0
    for c in required_columns:
        df = rm.summary(by=c)
        assert isinstance(df, pd.DataFrame)
        assert {c, "count", "mean"}.issubset(set(df.columns))
        assert len(df) > 0


def test_sale_commercial():
    """Test a search on commercial properties for sale."""
    url = f"{base_url}commercial-property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E70417"
    rm = RightmoveData(url)
    assert isinstance(rm.average_price, float)
    assert isinstance(rm.get_results, pd.DataFrame)
    assert required_columns.issubset(set(rm.get_results.columns))
    assert len(rm.get_results) > 0
    assert isinstance(rm.page_count, int)
    assert rm.is_commercial == True
    assert isinstance(rm.results_count, int)
    assert isinstance(rm.results_count_display, int)
    assert url == rm.url
    df = rm.summary()
    assert isinstance(df, pd.DataFrame)
    assert {"type", "count", "mean"}.issubset(set(df.columns))
    assert len(df) > 0
    for c in required_columns:
        if c == "number_bedrooms":
            continue
        df = rm.summary(by=c)
        assert isinstance(df, pd.DataFrame)
        assert {c, "count", "mean"}.issubset(set(df.columns))
        assert len(df) > 0


def test_rent_commercial():
    """Test a search on commercial properties for rent."""
    url = f"{base_url}commercial-property-to-let/find.html?searchType=RENT&locationIdentifier=REGION%5E70417"
    rm = RightmoveData(url)
    assert isinstance(rm.average_price, float)
    assert isinstance(rm.get_results, pd.DataFrame)
    assert required_columns.issubset(set(rm.get_results.columns))
    assert len(rm.get_results) > 0
    assert isinstance(rm.page_count, int)
    assert rm.is_commercial == True
    assert isinstance(rm.results_count, int)
    assert isinstance(rm.results_count_display, int)
    assert url == rm.url
    df = rm.summary()
    assert isinstance(df, pd.DataFrame)
    assert {"type", "count", "mean"}.issubset(set(df.columns))
    assert len(df) > 0
    for c in required_columns:
        if c == "number_bedrooms":
            continue
        df = rm.summary(by=c)
        assert isinstance(df, pd.DataFrame)
        assert {c, "count", "mean"}.issubset(set(df.columns))
        assert len(df) > 0


def test_bad_url():
    """Test a bad URL raises a value error."""
    bad_url = "https://www.rightmove.co.uk/property"
    with pytest.raises(ValueError):
        _ = RightmoveData(bad_url)
