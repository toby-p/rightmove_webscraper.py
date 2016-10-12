# right_move_web_scraper
Python function to scrape data from the <a href='http://www.rightmove.co.uk/'>rightmove.co.uk</a> property website, and save the results in a formatted CSV file for analysis.

## Background
This project originated when my sister was considering moving to London from Beijing and asked me how much she could expect to pay in rent for a 1-bedroom flat. I was about to say how much I currently pay and offer some baseless conjecture as to what I thought was roughly average, but I decided to try and find some hard data instead. After googling and coming up with some aggregate stats but no raw data, I wondered if I could turn this into a learning project to gain some new Python skills. I also happen to work in the property sector, and my company posts property listing on the rightmove.co.uk website, so I thought I could also tie it into my job by analysing the listings posted on that website.

## Function

The function I have written uses the <a href='https://pypi.python.org/pypi/lxml'>lxml</a> and <a href='https://pypi.python.org/pypi/requests/2.11.1'>requests</a> libraries to scrape data from the website. The steps to use the function are:

1. Go to rightmove.co.uk and perform whatever search you are interested in. For my purposes to answer my sister's question I have been searching for all rental residential properties in London.
2. After pressing search on the website you'll be shown the first page of matching results. Now copy and paste the full long URL from this page and set it as the first argument in the function.
3. For the function's second argument pass a string value of either 'rent' or 'buy', reflecting whatever it is you searched for.
4. Run the function and when finished it will output a time-stamped CSV file with all the results in columns showing:
 - price
 - type (i.e. studio, 1-bed, flatshare, etc.)
 - address
 - url of individual property listing
 - postcode
 - number_bedrooms
 - search date
 
The 'postcode' and 'number_bedrooms' columns are extracted from the 'address' and 'type' columns respectively using regular expressions, where possible, so will probably not be complete for every record.

## Repo contents

- <a href='https://github.com/woblers/right_move_web_scraper/blob/master/function_with_instructions.ipynb'>function_with_instructions.ipynb<a>
The function itself with explanation, example use, and error checking options.
- <a href='https://github.com/woblers/right_move_web_scraper/blob/master/rightmove_results_2016_10_07%2017%2000%2001.csv'>rightmove_results_2016_10_07 17 00 01.csv</a>
Results from the example in the function workbook.
- <a href = 'https://github.com/woblers/right_move_web_scraper/blob/master/analysis.ipynb'>analysis.ipynb</a>
Example analysis of results pulled from a search of London rental properties added over a 24 hour period, using the <a href='https://pypi.python.org/pypi/pandas/0.19.0'>pandas</a> package. I use an additional resource of all London postcodes to identify the London borough of each property listing (where possible from the postcode), and then summarise the results for 1-bedroom properties by borough; thus answering my sister's question!
- <a href='https://github.com/woblers/right_move_web_scraper/blob/master/london_postcodes.csv'>london_postcodes.csv</a>
File of all London Postcodes which is used in the analysis workbook.
- <a href='https://github.com/woblers/right_move_web_scraper/blob/master/london_data_script.py'>london_data_script.py</a>
Example of a full scipt that can be run from the terminal, which will scrape all London properties added to rent or buy in the past 24 hours.
- <a href = 'https://github.com/woblers/right_move_web_scraper/blob/master/london_buy.csv'>london_buy.csv</a>
Example output from the script of London properties to buy.
- <a href='https://github.com/woblers/right_move_web_scraper/blob/master/london_rent.csv'>london_rent.csv</a>
Example output from the script of London properties to rent.
- <a href 'https://github.com/woblers/right_move_web_scraper/blob/master/html.txt'>html.txt</a>
Example output of the full html file from the error checking code.

## To-Do list
I have some ideas to use this code and develop the project further, time permitting, including:
- Schedule a script to run every night collecting all new listings added that day, and upload them to a simple mysql database. This would allow for analysis of long-term property trends, and the data could be used by developers to identify hotspot areas, or by purchasers to find value in the market.
- Write an additional script to create alerts when new properties are added meeting a specified criteria.
- When collecting the results, iterate through each individual url to try to find longitude and latitude coordinates for each listing. This would take more time to run, but would be worth it to create maps visualising property prices and trends, e.g. using <a href='https://github.com/python-visualization/folium'>folium</a>.
- Write scripts/functions for alternative property listing websites to aggregate more market data.

## Feedback and contributions welcome!
