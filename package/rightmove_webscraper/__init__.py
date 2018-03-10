#!/usr/bin/env python3

# Dependencies
from lxml import html, etree
import requests
import pandas as pd
import datetime as dt

class _GetDataFromURL(object):
    """This "private" class does all the heavy lifting of fetching the data
    from the url provided, and then returns the relevant data to the 
    main rightmove_data class instance. The reason for this is so that all  
    the validation and web-scraping is done when an instance is created,  
    and afterwards the data is accessible quickly via methods on the 
    rightmove_data instance."""
    
    def __init__(self, url):
        self.url = url
        self.first_page = self.make_request(self.url)
        self.validate_url()
        self.get_results = self.__get_results
    
    def validate_url(self):
        """Basic validation that the URL at least starts in the right format
        and returns status code 200."""
        left_url = "http://www.rightmove.co.uk/property-{}/find.html?"
        types = ["to-rent", "for-sale"]
        conditions = [self.url.startswith(left_url.format(t)) for t in types]
        conditions.append(self.first_page[1] == 200)
        if not any(conditions):
            raise ValueError("This doesn't appear to be a valid rightmove.co.uk URL:\n\n\t{}".format(self.url))
    
    @property
    def rent_or_sale(self):
        """Tag to say whether the search is for properties for rent or sale.
        This is required beacuse the Xpaths are different for the target elements."""
        if "/property-for-sale/" in self.url:
             return "sale"
        elif "/property-to-rent/" in self.url:
            return "rent"

    @property
    def results_count(self):
        """Returns an integer of the total number of listings as displayed on the
        first page of results. Note that not all listings may be available to scrape 
        because rightmove limits the number of results pages which are accessible"""
        tree = html.fromstring(self.first_page[0])
        xpath = """//span[@class="searchHeader-resultCount"]/text()"""
        return int(tree.xpath(xpath)[0].replace(",", ""))
    
    @property
    def page_count(self):
        """Returns the number of result pages returned by the search URL.
        There are 24 results per page. Note that the website limits results
        to a maximum of 42 accessible pages."""
        page_count = self.results_count // 24
        if self.results_count % 24 > 0: page_count += 1
        # Rightmove will return a maximum of 42 results pages, hence:
        if page_count > 42: page_count = 42
        return page_count
    
    @staticmethod
    def make_request(url):
        r = requests.get(url)
        # Minimise the amount returned to reduce overheads:
        return r.content, r.status_code

    def get_page(self, request_content):
        """Method to scrape the data from a single page of search results.
        Used iteratively by the .get_results() method to scrape data from 
        every page returned by the search."""
        
        # Process the html:
        tree = html.fromstring(request_content)
        
        # Set xpath for price:
        if self.rent_or_sale == "rent":
            xp_prices = """//span[@class="propertyCard-priceValue"]/text()"""
        elif self.rent_or_sale == "sale":
            xp_prices = """//div[@class="propertyCard-priceValue"]/text()"""

        # Set xpaths for listing title, property address, URL, and agent URL:
        xp_titles = """//div[@class="propertyCard-details"]\
        //a[@class="propertyCard-link"]\
        //h2[@class="propertyCard-title"]/text()"""
        xp_addresses = """//address[@class="propertyCard-address"]//span/text()"""
        xp_weblinks = """//div[@class="propertyCard-details"]\
        //a[@class="propertyCard-link"]/@href"""
        xp_agent_urls = """//div[@class="propertyCard-contactsItem"]\
        //div[@class="propertyCard-branchLogo"]\
        //a[@class="propertyCard-branchLogo-link"]/@href"""

        # Create data lists from xpaths:
        price_pcm = tree.xpath(xp_prices)
        titles = tree.xpath(xp_titles)
        addresses = tree.xpath(xp_addresses)
        base = "http://www.rightmove.co.uk"
        weblinks = ["{}{}".format(base, tree.xpath(xp_weblinks)[w]) for w in range(len(tree.xpath(xp_weblinks)))]
        agent_urls = ["{}{}".format(base, tree.xpath(xp_agent_urls)[a]) for a in range(len(tree.xpath(xp_agent_urls)))]
        
        # Store the data in a Pandas DataFrame:
        data = [price_pcm, titles, addresses, weblinks, agent_urls]
        temp_df = pd.DataFrame(data)
        temp_df = temp_df.transpose()
        temp_df.columns = ["price", "type", "address", "url", "agent_url"]

        # Drop empty rows which come from placeholders in the html:
        temp_df = temp_df[temp_df["address"].notnull()]

        return temp_df
    
    @property
    def __get_results(self):
        """Returns a pandas DataFrame with all results returned by the search."""

        # Create DataFrame of the first page (which has already been requested):
        results = self.get_page(self.first_page[0])

        # Iterate through the rest of the pages scraping results:
        for p in range(1, self.page_count + 1, 1):

            # Create the URL of the specific results page:
            p_url = "{}&index={}".format(str(self.url), str((p * 24)))
            
            # Make the request:
            rc = self.make_request(p_url)
            
            # Requests to scrape lots of pages eventually get status 400, so:
            if rc[1] != 200: break
                
            # Create a temporary dataframe of page results:
            temp_df = self.get_page(rc[0])

            # Concatenate the temporary dataframe with the full dataframe:
            frames = [results, temp_df]
            results = pd.concat(frames)

        # Reset the index:
        results.reset_index(inplace = True, drop = True)

        # Convert price column to numeric type:
        results["price"].replace(regex = True, inplace = True, to_replace = r"\D", value = r"")
        results["price"] = pd.to_numeric(results["price"])

        # Extract postcodes to a separate column:
        pat = r"\b([A-Za-z][A-Za-z]?[0-9][0-9]?[A-Za-z]?)\b"
        results["postcode"] = results["address"].str.extract(pat, expand = True)

        # Extract number of bedrooms from "type" to a separate column:
        pat = r"\b([\d][\d]?)\b"
        results["number_bedrooms"] = results.type.str.extract(pat, expand = True)
        results.loc[results["type"].str.contains("studio", case = False), "number_bedrooms"] = 0
        
        # Clean up annoying white spaces and newlines in "type" column:
        for row in range(len(results)):
            type_str = results.loc[row, "type"]
            clean_str = type_str.strip("\n").strip()
            results.loc[row, "type"] = clean_str

        # Add column with datetime when the search was run (i.e. now):
        now = dt.datetime.today()
        results["search_date"] = now

        return results

class rightmove_data(object):
    """The rightmove_data web scraper works by implementing an instance of the class 
    on the URL returned by a search on the rightmove website. Go to rightmove.co.uk
    and search for whatever you want, then create an instance of the class on the URL 
    returned by the search. The class returns an object with attributes to access the 
    data from the search results, the most useful being .get_results, which returns
    all results as a pandas DataFrame object.
    """
    
    def __init__(self, url):
        self.__request_object = _GetDataFromURL(url)
        self.__url = url
        
    @property
    def url(self):
        return self.__url
    
    @property
    def get_results(self):
        """Returns a pandas DataFrame with all results returned by the search."""
        return self.__request_object.get_results
    
    @property
    def results_count(self):
        return len(self.get_results)
    
    @property
    def average_price(self):
        total = self.get_results["price"].dropna().sum()
        return int(total / self.results_count)
    
    def summary(self, by="number_bedrooms"):
        """Return a Pandas DataFrame summarising the the results by price.
        By default grouped by the number_bedrooms column but will accept 
        any column name from the .get_results DataFrame as a grouper."""
        df = self.get_results.dropna(axis=0, subset=["price"])
        groupers = {"price":["count", "mean"]}
        df = df.groupby(df[by]).agg(groupers).astype(int)
        df.columns = df.columns.get_level_values(1)
        df.reset_index(inplace = True)
        return df