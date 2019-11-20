# rightmove-webscraper

[![Downloads](https://pepy.tech/badge/rightmove-webscraper)](https://pepy.tech/project/rightmove-webscraper)

<a href="http://www.rightmove.co.uk/" target="_blank">rightmove.co.uk</a> is one of the UK's largest property listings websites, hosting thousands of listings of properties for sale and to rent.

<code>rightmove_webscraper.py</code> is a simple Python interface to scrape property listings from the website and prepare them in a Pandas dataframe for analysis.

## Installation

Version 1.0 is now available to install via Pip:

 <code>pip install -U rightmove-webscraper</code>

## How to use

1) Go to <a href="http://www.rightmove.co.uk/">rightmove.co.uk</a> and search for whatever listings you are interested in ...

<img src = "./docs/images/rightmove_search_screen.PNG">

2) Filter the search however you choose ...

<img src = "./docs/images/rightmove_search_screen_2.PNG">

<img src = "./docs/images/rightmove_search_screen_3.PNG">

3) Run the search and copy the URL of the results page ...

<img src = "./docs/images/rightmove_url.PNG">

4) Create an instance of the class on the URL ...

```python
from rightmove_webscraper import RightmoveData

url = "https://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E94346"
rm = RightmoveData(url)
```

5) Access the data using the methods and attributes of the object ...

<img src = "./docs/images/methods_attributes.png">

Get the average price of all listings returned by the search:

```python
rm.average_price
```
<img src = "./docs/images/av_price.png">


Show the total number of listings returned by the search:

```python
rm.results_count
```
<img src = "./docs/images/n_results.png">


Access the full results as a Pandas dataframe at the <code>.get_results</code> attribute.

```python
rm.get_results
```
<img src = "./docs/images/get_results.png">

Get quick summary statistics of the results, showing the number of listings and average price grouped by the number of bedrooms:

```python
rm.summary()
```
<img src = "./docs/images/summary.png">

Alternatively group the results by any other column returned in the <code>.get_results</code> DataFrame, for example Postcode:

```python
rm.summary(by="postcode")
```
<img src = "./docs/images/summary_by_postcode.png">

## Legal
<a href="https://github.com/toddy86">@toddy86</a> has pointed out per the terms and conditions <a href="https://www.rightmove.co.uk/this-site/terms-of-use.html"> here</a> the use of webscrapers is unauthorised by rightmove. So please don't use this package!
