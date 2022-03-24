# rightmove-webscraper

[![Downloads](https://pepy.tech/badge/rightmove-webscraper)](https://pepy.tech/project/rightmove-webscraper)

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

```python
from rightmove_webscraper import RightmoveData

url = "https://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E94346"
rm = RightmoveData(url)
```

## What will be scraped?

When a `RightmoveData` instance is created it automatically scrapes every page of results available from the search URL. However please note that rightmove restricts the total possible number of results pages to 42. Therefore if you perform a search which could theoretically return many thousands of results (e.g. "all rental properties in London"), in practice you are limited to only scraping the first 1050 results (42 pages * 25 listings per page = 1050 total listings). A couple of suggested workarounds to this limitation are:

* Reduce the search area and perform multiple scrapes, e.g. perform a search for each London borough instead of 1 search for all of London.
* Add a search filter to shorten the timeframe in which listings were posted, e.g. search for all listings posted in the past 24 hours, and schedule the scrape to run daily.

Finally, note that not every piece of data listed on the rightmove website is scraped, instead it is just a subset of the most useful features, such as price, address, number of bedrooms, listing agent. If there are additional data items you think should be scraped, please submit an issue or even better go find the xml path and submit a pull request with the changes.

## Accessing data 

The following instance methods and properties are available to access the scraped data.

**Full results as a Pandas.DataFrame**

```python
rm.get_results.head()
```

<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>price</th>      <th>type</th>      <th>address</th>      <th>url</th>      <th>agent_url</th>      <th>postcode</th>      <th>full_postcode</th>      <th>number_bedrooms</th>      <th>search_date</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>3400000.0</td>      <td>2 bedroom apartment for sale</td>      <td>Switch House East, Battersea Power Station, SW11</td>      <td>http://www.rightmove.co.uk/properties/121457195#/?channel=RES_BUY</td>      <td>http://www.rightmove.co.uk/estate-agents/agent/JLL/London-Residential-Developments-100183.html</td>      <td>SW11</td>      <td>NaN</td>      <td>2.0</td>      <td>2022-03-24 09:40:13.769706</td>    </tr>    <tr>      <th>1</th>      <td>11080000.0</td>      <td>Property for sale</td>      <td>Battersea Power Station, Circus Road East, London</td>      <td>http://www.rightmove.co.uk/properties/118473812#/?channel=RES_BUY</td>      <td>http://www.rightmove.co.uk/estate-agents/agent/Moveli/London-191324.html</td>      <td>NaN</td>      <td>NaN</td>      <td>NaN</td>      <td>2022-03-24 09:40:13.769706</td>    </tr>    <tr>      <th>2</th>      <td>9950000.0</td>      <td>5 bedroom apartment for sale</td>      <td>888 Scott House, Battersea Power Station, SW11</td>      <td>http://www.rightmove.co.uk/properties/89344718#/?channel=RES_BUY</td>      <td>http://www.rightmove.co.uk/estate-agents/agent/Prestigious-Property-Ltd/Ruislip-67965.html</td>      <td>SW11</td>      <td>NaN</td>      <td>5.0</td>      <td>2022-03-24 09:40:13.769706</td>    </tr>    <tr>      <th>3</th>      <td>9200000.0</td>      <td>3 bedroom penthouse for sale</td>      <td>Battersea Power Station, Nine Elms, London SW8</td>      <td>http://www.rightmove.co.uk/properties/114236963#/?channel=RES_BUY</td>      <td>http://www.rightmove.co.uk/estate-agents/agent/Copperstones/London-82091.html</td>      <td>SW8</td>      <td>NaN</td>      <td>3.0</td>      <td>2022-03-24 09:40:13.769706</td>    </tr>    <tr>      <th>4</th>      <td>9000000.0</td>      <td>6 bedroom apartment for sale</td>      <td>Scott House, Battersea Power Station, SW11</td>      <td>http://www.rightmove.co.uk/properties/107110697#/?channel=RES_BUY</td>      <td>http://www.rightmove.co.uk/estate-agents/agent/Dockleys/London-174305.html</td>      <td>SW11</td>      <td>NaN</td>      <td>6.0</td>      <td>2022-03-24 09:40:13.769706</td>    </tr>  </tbody></table>


**Average price of all listings scraped**

```python
rm.average_price
```

> `1650065.841025641`

**Total number of listings scraped**

```python
rm.results_count
```

> `195`

**Summary statistics** 

By default shows the number of listings and average price grouped by the number of bedrooms:

```python
rm.summary()
```

<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>number_bedrooms</th>      <th>count</th>      <th>mean</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>0</td>      <td>39</td>      <td>9.119231e+05</td>    </tr>    <tr>      <th>1</th>      <td>1</td>      <td>46</td>      <td>1.012935e+06</td>    </tr>    <tr>      <th>2</th>      <td>2</td>      <td>88</td>      <td>1.654237e+06</td>    </tr>    <tr>      <th>3</th>      <td>3</td>      <td>15</td>      <td>3.870867e+06</td>    </tr>    <tr>      <th>4</th>      <td>4</td>      <td>2</td>      <td>2.968500e+06</td>    </tr>    <tr>      <th>5</th>      <td>5</td>      <td>1</td>      <td>9.950000e+06</td>    </tr>    <tr>      <th>6</th>      <td>6</td>      <td>1</td>      <td>9.000000e+06</td>    </tr>  </tbody></table>

Alternatively group the results by any other column from the <code>.get_results</code> DataFrame, for example by postcode:

```python
rm.summary(by="postcode")
```

<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>postcode</th>      <th>count</th>      <th>mean</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>SW11</td>      <td>76</td>      <td>1.598841e+06</td>    </tr>    <tr>      <th>1</th>      <td>SW8</td>      <td>28</td>      <td>2.171357e+06</td>    </tr>  </tbody></table>

## Legal

<a href="https://github.com/toddy86">@toddy86</a> has pointed out per the terms and conditions <a href="https://www.rightmove.co.uk/this-site/terms-of-use.html"> here</a> the use of webscrapers is unauthorised by rightmove. So please don't use this package!
