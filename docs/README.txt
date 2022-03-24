# rightmove-webscraper

<a href="http://www.rightmove.co.uk/" target="_blank">rightmove.co.uk</a> is one of the UK's largest property listings websites, hosting thousands of listings of properties for sale and to rent.

<code>rightmove_webscraper.py</code> is a simple Python interface to scrape property listings from the website and prepare them in a Pandas dataframe for analysis.

## Installation

Version 1.1 is available to install via Pip:

 <code>pip install -U rightmove-webscraper</code>

## Scraping property listings

1) Go to <a href="http://www.rightmove.co.uk/">rightmove.co.uk</a> and search for whatever region, postcode, city, etc. you are interested in. You can also add any additional filters, e.g. property type, price, number of bedrooms, etc.

<img src = "./docs/images/rightmove_search_screen.PNG">

2) Run the search on the rightmove website and copy the URL of the first results page.

3) Create an instance of the class with the URL as the init argument.

` pythonfrom rightmove_webscraper import RightmoveData

url = "https://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E94346"
rm = RightmoveData(url) `

## What will be scraped?

When a `RightmoveData` instance is created it automatically scrapes every page of results available from the search URL. However please note that rightmove restricts the total possible number of results pages to 42. Therefore if you perform a search which could theoretically return many thousands of results (e.g. "all rental properties in London"), in practice you are limited to only scraping the first 1050 results (42 pages * 25 listings per page = 1050 total listings). A couple of suggested workarounds to this limitation are:

* Reduce the search area and perform multiple scrapes, e.g. perform a search for each London borough instead of 1 search for all of London.
* Add a search filter to shorten the timeframe in which listings were posted, e.g. search for all listings posted in the past 24 hours, and schedule the scrape to run daily.

Finally, note that not every piece of data listed on the rightmove website is scraped, instead it is just a subset of the most useful features, such as price, address, number of bedrooms, listing agent. If there are additional data items you think should be scraped, please submit an issue or even better go find the xml path and submit a pull request with the changes.

## Accessing data

The following instance methods and properties are available to access the scraped data.

**Full results as a Pandas.DataFrame**

` python
rm.get_results.head()
`

**Average price of all listings scraped**

` python
rm.average_price
`

> ` 1650065.841025641 `

**Total number of listings scraped**

` python
rm.results_count
`

> ` 195 `

**Summary statistics**

By default shows the number of listings and average price grouped by the number of bedrooms:

` python
rm.summary()
`

Alternatively group the results by any other column from the <code>.get_results</code> DataFrame, for example by postcode:

` python
rm.summary(by="postcode")
`

## Legal

<a href="https://github.com/toddy86">@toddy86</a> has pointed out per the terms and conditions <a href="https://www.rightmove.co.uk/this-site/terms-of-use.html"> here</a> the use of webscrapers is unauthorised by rightmove. So please don't use this package!
