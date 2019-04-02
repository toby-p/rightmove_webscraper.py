# rightmove_webscraper

<a href="http://www.rightmove.co.uk/" target="_blank">rightmove.co.uk</a> is one of the UK's largest property listings websites, hosting thousands of listings of properties for sale and to rent.

<code>rightmove_webscraper.py</code> is a simple Python interface to scrape property listings from the website and prepare them in a Pandas dataframe for analysis.

## Installation

Version 0.3 is now available as a package with all required dependencies on Pip.

Install with:

 <code>pip install -U rightmove-webscraper</code>

## How to use

1) Go to <a href="http://www.rightmove.co.uk/">rightmove.co.uk</a> and search for whatever listings you are interested in ...

<img src = "./images/rightmove_search_screen.PNG">

2) Filter the search however you choose ...

<img src = "./images/rightmove_search_screen_2.PNG">

<img src = "./images/rightmove_search_screen_3.PNG">

3) Run the search and copy the URL of the results page ...

<img src = "./images/rightmove_url.PNG">

4) Create an instance of the class on the URL ...

```python
from rightmove_webscraper import rightmove_data
url = "http://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier= [...] "
rightmove_object = rightmove_data(url)
```

5) Access the data using the methods and attributes of the object ...

<img src = "./images/methods_and_attributes.PNG">

Find the average price of all listings returned by the search:

```python
rightmove_object.average_price
```
<img src = "./images/average_price.PNG">


Show the total number of listings returned by the search:

```python
rightmove_object.results_count
```
<img src = "./images/number_results.PNG">


Access the full results as a Pandas dataframe with the <code>.get_results</code> attribute.

```python
rightmove_object.get_results
```
<img src = "./images/results_dataframe.PNG">

Get quick summary statistics of the results, showing the number of listings and average price grouped by the number of bedrooms:

```python
rightmove_object.summary()
```
<img src = "./images/summary_default.PNG">

Alternatively group the results by any other column returned in the <code>.get_results</code> DataFrame, for example Postcode:

```python
rightmove_object.summary(by = "postcode")
```
<img src = "./images/summary_postode.PNG">

## Legal
<a href="https://github.com/toddy86">@toddy86</a> has pointed out per the terms and conditions <a href="https://www.rightmove.co.uk/this-site/terms-of-use.html"> here</a> the use of webscrapers is unauthorised by rightmove. So please don't use this package!
