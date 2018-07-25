#!/usr/bin/env python3

from rightmove_webscraper import rightmove_data
from pandas import DataFrame

def test_valid_urls(urls):
    for u in urls:
        print("Testing URL: {} ...".format(u))
        try:
            data = rightmove_data(u)
            if len(data.get_results) > 0:
                print("> Passed - collected results.")
                print("Testing object attributes ...")
                check_all_attrs(data)
                print("Testing object methods ...")
                if isinstance(data.summary(), DataFrame):
                    print("method: summary()\n> Passed - returned type {}".format(DataFrame))
                else:
                    print("method: summary()\n> FAILED - did not return type {}".format(DataFrame))
            else:
                print("> FAILED - no results collected.")
                
        except Exception as e:
            print("Testing URL: {}\n> FAILED with Exception:\n\t{}".format(u, e))
        print()

def check_attribute(rightmove_data_object, attr_name, attr_type):
    val = getattr(rightmove_data_object, attr_name)
    if isinstance(val, attr_type):
        print("attr: {}\n> Passed - returned type {}".format(attr_name, attr_type))
    else:
        print("attr: {}\n> FAILED - did not return type {}".format(attr_name, attr_type))

def check_all_attrs(rightmove_data_object):
    valid_types = {"average_price":int,
                   "get_results":DataFrame,
                   "results_count":int,
                   "url":str}
    
    for k in valid_types:
        check_attribute(rightmove_data_object, k, valid_types[k])
            

def test_invalid_urls(urls):
    for u in urls:
        try:
            data = rightmove_data(u)
            if len(data.get_results)>0:
                print("Testing URL: {}\n> FAILED - created results with invalid URL.".format(u))
            else:
                print("Testing URL: {}\n> Passed - no results collected.".format(u))
        except Exception as e:
            print("Testing URL: {}\n> Passed - raised Exception.".format(u))
        print()

urls = ["https://www.rightmove.co.uk/new-homes-for-sale/find.html?locationIdentifier=REGION%5E70417&includeSSTC=false",
       "https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier=REGION%5E70417&insId=1&radius=0.0",
       "https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E70417&maxDaysSinceAdded=7&includeSSTC=false"]
test_valid_urls(urls)

urls = ["https://www.rightmove.co.uk/stupidrightmove/find.html?locationIdentifier=REGION%5E70417&includeSSTC=false",
       "https://www.google.com",
       "just not a URL at all "]
test_invalid_urls(urls)    