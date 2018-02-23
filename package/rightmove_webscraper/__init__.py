#!/usr/bin/env python

# Dependencies
from lxml import html, etree
import requests
import pandas as pd
import datetime as dt

class rightmove_data(object):
    """The rightmove_data web scraper works by implementing an instance of the class 
    on the URL returned by a search on the rightmove website. Go to rightmove.co.uk
    and search for whatever you want, then create an instance of the class on the URL 
    returned by the search. The class returns an object which includes various 
    methods for extracting data from the search results, the most useful being the 
    .get_results() method which returns all results as a pandas DataFrame object.
    """
    
    def __init__(self, url):
        
        self.url = url
        
        try:
            if "searchType=SALE" in self.url:
                self.rent_or_sale = "SALE"
            elif "searchType=RENT" in self.url:
                self.rent_or_sale = "RENT"
        except ValueError:
            print("Not a valid rightmove search URL.")
        
        self.results_count = self.__results_count()
        self.result_pages_count = self.__result_pages_count()


    def __results_count(self):
        """Returns an integer of the total number of results returned by the search URL."""
        
        page = requests.get(self.url)
        tree = html.fromstring(page.content)
        xp_result_count = """//span[@class="searchHeader-resultCount"]/text()"""
        return int(tree.xpath(xp_result_count)[0].replace(",", ""))

    
    def __result_pages_count(self):
        """Returns the number of result pages returned by the search URL.
        There are 24 results on each results page, but note that the
        rightmove website limits results pages to a maximum of 42 pages."""

        page_count = self.results_count // 24
        
        if self.results_count % 24 > 0:
            page_count += 1

        # Rightmove will return a maximum of 42 results pages, hence:
        if page_count > 42: page_count = 42

        return page_count

    
    def __get_page_results(self,page_url):
        """This is a hidden method to scrape the data from a single page
        of search results. It is used iteratively by the .get_results()
        method to scrape data from every page returned by the search."""

        # Set the correct xpath for the price.
        if self.rent_or_sale == "RENT":
            xp_prices = """//span[@class="propertyCard-priceValue"]/text()"""
        elif self.rent_or_sale == "SALE":
            xp_prices = """//div[@class="propertyCard-priceValue"]/text()"""

        # Set the xpaths for listing title, property address, 
        # listing URL, and agent URL.
        xp_titles = """//div[@class="propertyCard-details"]\
        //a[@class="propertyCard-link"]\
        //h2[@class="propertyCard-title"]/text()"""
        xp_addresses = """//address[@class="propertyCard-address"]//span/text()"""
        xp_weblinks = """//div[@class="propertyCard-details"]\
        //a[@class="propertyCard-link"]/@href"""
        xp_agent_urls = """//div[@class="propertyCard-contactsItem"]\
        //div[@class="propertyCard-branchLogo"]\
        //a[@class="propertyCard-branchLogo-link"]/@href"""

        # Use the requests library to get the whole web page.
        page = requests.get(page_url)

        # Process the html.
        tree = html.fromstring(page.content)
        
        # Create data lists from Xpaths.
        price_pcm = tree.xpath(xp_prices)
        titles = tree.xpath(xp_titles)
        addresses = tree.xpath(xp_addresses)
        urlbase = "http://www.rightmove.co.uk"
        weblinks = ["{}{}".format(urlbase, tree.xpath(xp_weblinks)[val]) \
                    for val in range(len(tree.xpath(xp_weblinks)))]
        agent_urls = ["{}{}".format(urlbase, tree.xpath(xp_agent_urls)[val]) \
                      for val in range(len(tree.xpath(xp_agent_urls)))]
        
        # Store the data in a temporary pandas DataFrame.
        data = [price_pcm, titles, addresses, weblinks, agent_urls]
        temp_df = pd.DataFrame(data)
        temp_df = temp_df.transpose()
        temp_df.columns = ["price", "type", "address", "url", "agent_url"]

        # Drop empty rows which come from placeholders in the html.
        temp_df = temp_df[temp_df["address"].notnull()]

        return temp_df

    
    def get_results(self):
        """Returns a pandas DataFrame with all results returned by the search."""

        # Create DataFrame to store results.
        full_results = pd.DataFrame(columns={"price", "type", "address", "url", "agent_url"})

        # Iterate through pages of results, using the .__get_page_results method to scrape results.
        for page in range(0, self.result_pages_count+1, 1):

            # Create the URL of the specific results page.
            iteration_url = "{}{}{}".format(str(self.url), "&index=", str((page*24)))

            # Create a temporary dataframe of the page results.
            temp_df = self.__get_page_results(iteration_url)

            # Concatenate the temporary dataframe with the full dataframe.
            frames = [full_results, temp_df]
            full_results = pd.concat(frames)

        # Reset the index.
        full_results = full_results.reset_index(drop=True)

        # Convert price column to numeric type.
        full_results.price.replace(regex=True, inplace=True, to_replace=r"\D", value=r"")
        full_results.price = pd.to_numeric(full_results.price)

        # Extract postcodes to a separate column.
        full_results["postcode"] = full_results["address"].str.extract\
        (r"\b([A-Za-z][A-Za-z]?[0-9][0-9]?[A-Za-z]?)\b", expand=True)

        # Extract number of bedrooms from "type" to a separate column.
        full_results["number_bedrooms"] = full_results.type.str.extract(r"\b([\d][\d]?)\b", expand=True)
        full_results.loc[full_results["type"].str.contains("studio", case=False), "number_bedrooms"]=0
        
        # Clean up annoying white spaces and newlines in "type" column.
        for row in range(len(full_results)):
            type_str = full_results.loc[row, "type"]
            clean_str = type_str.strip("\n").strip()
            full_results.loc[row, "type"] = clean_str

        # Add column with datetime when the search was run (i.e. now).
        now = dt.datetime.today()
        full_results["search_date"] = now

        return full_results