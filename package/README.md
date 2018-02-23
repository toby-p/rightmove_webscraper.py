# rightmove_webscraper

<a href="http://www.rightmove.co.uk/">rightmove.co.uk</a> is one of the UK's largest property listings websites, hosting thousands of  listings of properties for sale and to rent.

The <code>rightmove_webscraper.py</code> class is a simple Python interface to scrape property listings from the website and prepare them in a Pandas dataframe for analysis.

The class uses the <i>lxml</i> and <i>requests</i> libraries to scrape data from the rightmove website.

Note the module has been built and tested in Python 3 only.

## How to use

1) Go to <a href="http://www.rightmove.co.uk/">rightmove.co.uk</a> and search for whatever listings you are interested in ...

2) Filter the search however you choose ...

3) Run the search and copy the URL of the results page ...

4) Create an instance of the class on the URL ...

```python
url = "http://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier= [...] "
rightmove_object = rightmove_data(url)
```

5) Access the data using the methods and attributes of the object ...

For example; the full results can be created as a Pandas dataframe using the <code>.get_results()</code> method.