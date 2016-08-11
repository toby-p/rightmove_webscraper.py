# right_move_web_scraper
Function to pull data from rightmove.co.uk property search and convert results to pandas dataframe for analysis.

Background

My sister was considering moving to London and was asking me about how much she could expect to be paying in rent. I was going to give a handwavy answer based on what I currently pay and a few other flats I've looked at recently, but then decided that as a data analyst by trade I should really give a data-driven answer.

After googling for data sources I found some aggregated statistics but little raw data, so while I continue to work on my python skills I decided to try and build my own program to collect the raw data from a popular property listing website.


Functionality

The program is designed to work on any search url returned by the rightmove.co.uk website. In the example workbook I have performed a search for residential properties to rent in the London Fields area, added to the site in the last 7 days. You then simply copy the website into a variable and call the function on that variable (or just call the function directly on the url string). The function will return a pandas dataframe of all the results returned by the search query, with columns for price (converted to numeric type for easier analysis), property type, address, and URL for the specific property listing. The dataframe also returns a column with today's date, so that searches over time could be aggregated for time-series analysis.



Future development plans for this include:

- write a regex function to extract postcodes from the address field.
- link up the postcode data to secondary data source to get the London borough for each property.
- schedule the function to automatically run daily for all new rental properties added in London, to build up a proper database.
- proper analysis and visualisation of the results!


Credits

Function is built for use on the property website rightmove:
http://www.rightmove.co.uk/

In writing the function I found this succinct tutorial on building python webscrapers very helpful:
http://docs.python-guide.org/en/latest/scenarios/scrape/

The W3 tutorial on Xpath was great help in understanding how this syntax works:
http://www.w3schools.com/xsl/xpath_intro.asp

And stackoverflow, obviously.
