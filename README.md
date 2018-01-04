# rightmove_webscraper

<a href="http://www.rightmove.co.uk/" target="_blank">rightmove.co.uk</a> is one of the UK's largest property listings websites, hosting thousands of  listings of properties for sale and to rent.

The <code>rightmove_webscraper.py</code> class is a simple Python interface to scrape property listings from the website and prepare them in a Pandas dataframe for analysis.

The class uses the <i>lxml</i> and <i>requests</i> libraries to scrape data from the rightmove website. 

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
url = "http://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier= [...] "
rightmove_object = rightmove_data(url)
```

5) Access the data using the methods and attributes of the object ...

<img src = "./images/methods_and_attributes.PNG">

The full results can be created as a Pandas dataframe using the <code>.get_results()</code> method.

<img src = "./images/results_dataframe.PNG">
