# Data Analyst Portfolio

## Thrift Store Project
This ongoing project is meant to create a search function allowing the user to search the ZIP code of a thrift store and see the percentile scores of four categories of thrift shopping in that ZIP code. Also visualizations of demographics information are presented.

## Technical Skills Utilized
* Python
* Data Visualization using matplotlib, and seaborn (examples in files) 
* Data analysis using pandas, numpy, and scipy.stats.
* Excel formulas and references (for creating the csv that the program uses)
* Tableau Income and Age Maps available [here](https://public.tableau.com/app/profile/alexander.adams3449).

## Process
The data used for [master_thrift_store.csv](https://github.com/aadams10046/Thrift-Store-Python-Project/blob/main/master_thrift_store.csv) was pulled from Census.gov data collected in 2020. Some ZIP codes had no data collected for income or median age. In these cases I did one of two things: 
1. If a city had two or more ZIPS that had data, I used the mean average of the other data points for that ZIP.
2. Otherwise, I used the average of that column for the whole state.
Since the point of the exercise was about finding the best thrift stores and scoring the thrift stores in a certain ZIP, this essentially removed these ZIPs with missing information from the "Best of" and "Worst of" lists and made their scores completely average. 

I then used [APIFY's Google Maps Scraper](https://console.apify.com/) to pull the list of all thrift stores and clothes resale shops in Michigan; this created [thrift_stores.csv](https://github.com/aadams10046/Thrift-Store-Python-Project/blob/main/thrift_stores.csv). I used all of this generated information to generate the count of all thrift stores after cleaning the scraper-generated data, thus creating [Business_Count_by_ZIP.csv](https://github.com/aadams10046/Thrift-Store-Python-Project/blob/main/Business_Count_by_ZIP.csv).
Once this was complete I used SQL to join the business count and master list data into [master_thrift_store_with_count.csv](https://github.com/aadams10046/Thrift-Store-Python-Project/blob/main/master_thrift_store_with_count.csv). Once complete, I used this information to build the Tableau vizualizations linked above.

## Full SQL Code with comments [here](https://github.com/aadams10046/Thrift-Store-Python-Project/blob/main/Lookup.sql)

## Full Python Code with comments [here](https://github.com/aadams10046/Thrift-Store-Python-Project/blob/main/Data_Boy.py)
