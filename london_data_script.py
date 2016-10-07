#!/usr/bin/env python

# imports
from lxml import html, etree
import requests
import pandas as pd
import datetime as dt

def rightmove_webscrape(rightmove_url,rent_or_buy):

# Get the start & end of the web url around the index value
    start,end = rightmove_url.split('&index=')
    url_start = start+'&index='
    url_end = end[1:]

# Initialise variables
    price_pcm=[]
    titles=[]
    addresses=[]
    weblinks=[]
    page_counts=[]

# Initialise pandas DataFrame for results.
    df=pd.DataFrame(columns=['price','type','address','url'])

# Get the total number of results from the search
    page = requests.get(rightmove_url)
    tree = html.fromstring(page.content)
    xp_result_count = '//span[@class="searchHeader-resultCount"]/text()'
    result_count = int(tree.xpath(xp_result_count)[0].replace(",", ""))

# Turn the total number of search results into number of iterations for the loop
    loop_count = result_count/24
    if result_count%24>0:
        loop_count = loop_count+1

# Set the Xpath variables for the loop
    if rent_or_buy=='rent':
        xp_prices = '//span[@class="propertyCard-priceValue"]/text()'
    elif rent_or_buy=='buy':
        xp_prices = '//div[@class="propertyCard-priceValue"]/text()'

    xp_titles = '//div[@class="propertyCard-details"]//a[@class="propertyCard-link"]//h2[@class="propertyCard-title"]/text()'
    xp_addresses = '//address[@class="propertyCard-address"]/text()'
    xp_weblinks = '//div[@class="propertyCard-details"]//a[@class="propertyCard-link"]/@href'

# Start the loop through the search result web pages
    for pages in range(0,loop_count,1):
        rightmove_url = url_start+str(pages*24)+url_end
        page = requests.get(rightmove_url)
        tree = html.fromstring(page.content)

# Reset variables
        price_pcm=[]
        titles=[]
        addresses=[]
        weblinks=[]

# Create data lists from Xpaths
        for val in tree.xpath(xp_prices):
            price_pcm.append(val)
        for val in tree.xpath(xp_titles):
            titles.append(val)
        for val in tree.xpath(xp_addresses):
            addresses.append(val)
        for val in tree.xpath(xp_weblinks):
            weblinks.append(val)

# Convert data to temporary DataFrame
        data = [price_pcm, titles, addresses, weblinks]
        temp_df= pd.DataFrame(data)
        temp_df = temp_df.transpose()
        temp_df.columns=['price','type','address','url']

# Drop empty rows from DataFrame which come from placeoholders in html file.
        temp_df = temp_df[temp_df.url != '/property-for-sale/property-0.html']

# Join temporary DataFrame to main results DataFrame.
        frames = [df,temp_df]
        df = pd.concat(frames)

# Renumber results DataFrame index to remove duplicate index values.
    df = df.reset_index(drop=True)

# Convert price column to numeric values for analysis.
    df.price.replace(regex=True,inplace=True,to_replace=r'\D',value=r'')
    df.price=pd.to_numeric(df.price)

# Extract postcode areas to separate column.
    df['postcode'] = df['address'].str.extract(r'\b([A-Za-z][A-Za-z]?[0-9][0-9]?[A-Za-z]?)\b',expand=True)

# Extract number of bedrooms from 'type' column.
    df['number_bedrooms'] = df.type.str.extract(r'\b([\d][\d]?)\b',expand=True)
    df.loc[df['type'].str.contains('studio',case=False),'number_bedrooms']=0

# Add in search_date column with date website was queried (i.e. today's date).
    now = dt.datetime.today().strftime("%d/%m/%Y")
    df['search_date'] = now

# Optional line to export the results to CSV if you wish to inspect them in an alternative program.
#     df.to_csv('rightmove_df.csv',encoding='utf-8')

    print 'The search returned a total of ', len(df),' results.'
    return df

# Urls to scrape - all London properties added to the site in the last 24 hours
rent_url = 'http://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E87490&numberOfPropertiesPerPage=24&radius=0.0&sortType=6&index=0&propertyTypes=detached%2Csemi-detached%2Cterraced%2Cflat%2Cbungalow&maxDaysSinceAdded=1&includeLetAgreed=false&viewType=LIST&areaSizeUnit=sqft&currencyCode=GBP'
buy_url = 'http://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E87490&numberOfPropertiesPerPage=24&radius=0.0&sortType=2&index=0&propertyTypes=detached%2Csemi-detached%2Cterraced%2Cflat%2Cbungalow&maxDaysSinceAdded=1&includeSSTC=false&viewType=LIST&areaSizeUnit=sqft&currencyCode=GBP'

df = rightmove_webscrape(rent_url,'rent')
df.to_csv('london_rent.csv',encoding='utf-8')
df = rightmove_webscrape(buy_url,'buy')
df.to_csv('london_buy.csv',encoding='utf-8')
