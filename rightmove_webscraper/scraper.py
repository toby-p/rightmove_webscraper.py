
import datetime
from lxml import html
import numpy as np
import pandas as pd
import requests


class RightmoveData:
    """The `RightmoveData` webscraper collects structured data on properties
    returned by a search performed on www.rightmove.co.uk

    An instance of the class provides attributes to access data from the search
    results, the most useful being `get_results`, which returns all results as a
    Pandas DataFrame object.

    The query to rightmove can be renewed by calling the `refresh_data` method.
    """
    def __init__(self, url: str, get_floorplans: bool = False):
        """Initialize the scraper with a URL from the results of a property
        search performed on www.rightmove.co.uk.

        Args:
            url (str): full HTML link to a page of rightmove search results.
            get_floorplans (bool): optionally scrape links to the individual
                floor plan images for each listing (be warned this drastically
                increases runtime so is False by default).
        """
        self._status_code, self._first_page = self._request(url)
        self._url = url
        self._validate_url()
        self._results = self._get_results(get_floorplans=get_floorplans)

    @staticmethod
    def _request(url: str):
        r = requests.get(url)
        return r.status_code, r.content

    def refresh_data(self, url: str = None, get_floorplans: bool = False):
        """Make a fresh GET request for the rightmove data.

        Args:
            url (str): optionally pass a new HTML link to a page of rightmove
                search results (else defaults to the current `url` attribute).
            get_floorplans (bool): optionally scrape links to the individual
                flooplan images for each listing (this drastically increases
                runtime so is False by default).
        """
        url = self.url if not url else url
        self._status_code, self._first_page = self._request(url)
        self._url = url
        self._validate_url()
        self._results = self._get_results(get_floorplans=get_floorplans)

    def _validate_url(self):
        """Basic validation that the URL at least starts in the right format and
        returns status code 200."""
        real_url = "{}://www.rightmove.co.uk/{}/find.html?"
        protocols = ["http", "https"]
        types = ["property-to-rent", "property-for-sale", "new-homes-for-sale"]
        urls = [real_url.format(p, t) for p in protocols for t in types]
        conditions = [self.url.startswith(u) for u in urls]
        conditions.append(self._status_code == 200)
        if not any(conditions):
            raise ValueError(f"Invalid rightmove search URL:\n\n\t{self.url}")

    @property
    def url(self):
        return self._url

    @property
    def get_results(self):
        """Pandas DataFrame of all results returned by the search."""
        return self._results

    @property
    def results_count(self):
        """Total number of results returned by `get_results`. Note that the
        rightmove website may state a much higher number of results; this is
        because they artificially restrict the number of results pages that can
        be accessed to 42."""
        return len(self.get_results)

    @property
    def average_price(self):
        """Average price of all results returned by `get_results` (ignoring
        results which don't list a price)."""
        total = self.get_results["price"].dropna().sum()
        return total / self.results_count

    def summary(self, by: str = None):
        """DataFrame summarising results by mean price and count. Defaults to
        grouping by `number_bedrooms` (residential) or `type` (commercial), but
        accepts any column name from `get_results` as a grouper.

        Args:
            by (str): valid column name from `get_results` DataFrame attribute.
        """
        if not by:
            by = "type" if self.is_commercial else "number_bedrooms"
        assert by in self.get_results.columns, f"Column not found in `get_results`: {by}"
        df = self.get_results.dropna(axis=0, subset=["price"])
        groupers = {"price": ["count", "mean"]}
        df = df.groupby(df[by]).agg(groupers)
        df.columns = df.columns.get_level_values(1)
        df.reset_index(inplace=True)
        if "number_bedrooms" in df.columns:
            df["number_bedrooms"] = df["number_bedrooms"].astype(int)
            df.sort_values(by=["number_bedrooms"], inplace=True)
        else:
            df.sort_values(by=["count"], inplace=True, ascending=False)
        return df.reset_index(drop=True)

    @property
    def is_commercial(self):
        """Boolean specifying if the search is for commercial properties."""
        if "/property-for-sale/" in self.url or "/new-homes-for-sale/" in self.url or "/property-to-rent/" in self.url:
            return False
        elif "/commercial-property-for-sale/" in self.url or "/commercial-property-to-let/" in self.url:
            return True
        else:
            raise ValueError(f"Invalid rightmove URL:\n\n\t{self.url}")

    @property
    def results_count_display(self):
        """Returns an integer of the total number of listings as displayed on
        the first page of results. Note that not all listings are available to
        scrape because rightmove limits the number of accessible pages."""
        tree = html.fromstring(self._first_page)
        xpath = """//div[contains(@class,"ResultsCount_resultsCount__")]//p//span/text()"""
        return int(tree.xpath(xpath)[0].replace(",", ""))

    @property
    def page_count(self):
        """Returns the number of result pages returned by the search URL. There
        are 24 results per page. Note that the website limits results to a
        maximum of 42 accessible pages."""
        page_count = self.results_count_display // 24
        if self.results_count_display % 24 > 0:
            page_count += 1
        # Rightmove will return a maximum of 42 results pages, hence:
        if page_count > 42:
            page_count = 42
        return page_count

    def _get_page(self, request_content: str, get_floorplans: bool = False):
        """Method to scrape data from a single page of search results. Used
        iteratively by the `get_results` method to scrape data from every page
        returned by the search."""
        # Process the html:
        tree = html.fromstring(request_content)

        # Find all property card containers and extract data per-card.
        # This ensures fields like bedroom count (which may be missing) stay aligned with the correct data row.
        cards = tree.xpath("""//div[contains(@class, "propertyCard-details")]""")

        price_pcm = []
        types = []
        addresses = []
        weblinks = []
        agent_urls = []
        number_bedrooms = []
        base = "http://www.rightmove.co.uk"

        for card in cards:
            price = card.xpath('.//div[contains(@class, "PropertyPrice_price__")]/text()')
            price_pcm.append(price[0] if price else None)

            prop_type = card.xpath('.//span[contains(@class, "PropertyInformation_propertyType__")]/text()')
            types.append(prop_type[0] if prop_type else None)

            address = card.xpath('.//address[contains(@class, "PropertyAddress_address__")]/text()')
            addresses.append(address[0] if address else None)

            link = card.xpath('.//a[@class="propertyCard-link"]/@href')
            weblinks.append(f"{base}{link[0]}" if link else None)

            agent_url = card.xpath('.//div[contains(@class,"PropertyCardActions_estateAgent__")]//a/@href')
            agent_urls.append(f"{base}{agent_url[0]}" if agent_url else None)

            bedrooms = card.xpath('.//span[contains(@class, "PropertyInformation_bedroomsCount__")]/text()')
            number_bedrooms.append(bedrooms[0] if bedrooms else None)

        print(f"Scraped {len(cards)} listings from page.")
        print(f"price_pcm: {len(price_pcm)}, types: {len(types)}, addresses: {len(addresses)}, weblinks: {len(weblinks)}, agent_urls: {len(agent_urls)}, number_bedrooms: {len(number_bedrooms)}")

        # Optionally get floorplan links from property urls (longer runtime):
        floorplan_urls = list() if get_floorplans else np.nan
        if get_floorplans:
            for weblink in weblinks:
                status_code, content = self._request(weblink)
                if status_code != 200:
                    continue
                tree = html.fromstring(content)
                xp_floorplan_url = """//*[@id="floorplanTabs"]/div[2]/div[2]/img/@src"""
                floorplan_url = tree.xpath(xp_floorplan_url)
                if floorplan_url:
                    floorplan_urls.append(floorplan_url[0])
                else:
                    floorplan_urls.append(np.nan)

        # Store the data in a Pandas DataFrame:
        data = [price_pcm, types, addresses, weblinks, agent_urls, number_bedrooms]
        data = data + [floorplan_urls] if get_floorplans else data
        temp_df = pd.DataFrame(data)
        temp_df = temp_df.transpose()
        columns = ["price", "type", "address", "url", "agent_url", "number_bedrooms"]
        columns = columns + ["floorplan_url"] if get_floorplans else columns
        temp_df.columns = columns

        # Drop empty rows which come from placeholders in the html:
        temp_df = temp_df[temp_df["address"].notnull()]

        return temp_df

    def _get_results(self, get_floorplans: bool = False):
        """Build a Pandas DataFrame with all results returned by the search."""
        results = self._get_page(self._first_page, get_floorplans=get_floorplans)

        # Iterate through all pages scraping results:
        for p in range(1, self.page_count + 1, 1):

            # Create the URL of the specific results page:
            p_url = f"{str(self.url)}&index={p * 24}"

            # Make the request:
            status_code, content = self._request(p_url)

            # Requests to scrape lots of pages eventually get status 400, so:
            if status_code != 200:
                break

            # Create a temporary DataFrame of page results:
            temp_df = self._get_page(content, get_floorplans=get_floorplans)

            # Concatenate the temporary DataFrame with the full DataFrame:
            frames = [results, temp_df]
            results = pd.concat(frames)

        return self._clean_results(results)

    @staticmethod
    def _clean_results(results: pd.DataFrame):
        # Reset the index:
        results.reset_index(inplace=True, drop=True)

        # Convert price column to numeric type:
        results["price"].replace(regex=True, inplace=True, to_replace=r"\D", value=r"")
        results["price"] = pd.to_numeric(results["price"])

        # Extract short postcode area to a separate column:
        pat = r"\b([A-Za-z][A-Za-z]?[0-9][0-9]?[A-Za-z]?)\b"
        results["postcode"] = results["address"].astype(str).str.extract(pat, expand=True)[0]

        # Extract full postcode to a separate column:
        pat = r"([A-Za-z][A-Za-z]?[0-9][0-9]?[A-Za-z]?[0-9]?\s[0-9]?[A-Za-z][A-Za-z])"
        results["full_postcode"] = results["address"].astype(str).str.extract(pat, expand=True)[0]

        # Record 'studio' properties as having 0 bedrooms:
        results.loc[results["type"].str.contains("studio", case=False), "number_bedrooms"] = "0"

        # Clean up annoying white spaces and newlines in `type` column:
        results["type"] = results["type"].str.strip("\n").str.strip()

        # Add column with datetime when the search was run (i.e. now):
        now = datetime.datetime.now()
        results["search_date"] = now

        return results
