# rightmove_webscraper
A Python class to scrape data from the <a href='http://www.rightmove.co.uk/'>rightmove.co.uk</a> property website and save the results in a pandas DataFrame object.

## How to use

The class uses the <a href='https://pypi.python.org/pypi/lxml'>lxml</a> and <a href='https://pypi.python.org/pypi/requests/2.11.1'>requests</a> libraries to scrape data from the rightmove website. The necessary steps to use the class are:

1. Go to rightmove.co.uk and perform whatever search you are interested in.
2. After searching on the website you'll be shown the first page of matching results - copy and paste the full long URL, and create an instance of the class on the URL.
