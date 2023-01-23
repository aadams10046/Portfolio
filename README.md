# Data Analyst Portfolio
This ongoing project is meant to create a search function allowing the user to search the ZIP code of a thrift store and see the percentile scores of four categories of thrift shopping in that ZIP code. Also visualizations of demographics information are presented.

## Technical Skills Utilized
* Python
* Data Visualization using numpy, scipy.stats, matplotlib, and seaborn (examples in files) 
* Data analysis using pandas
* Excel (for creating the csv that the program uses)
* Tableau Income and Age Maps available [here](https://public.tableau.com/app/profile/alexander.adams3449/viz/MichiganMaps/Income).

## Notes
The data used for the initial .csv was pulled from Census.gov data collected in 2020. Some ZIP codes had no data collected for income or median age. In these cases I did one of two things: 
* (1) If a city had two or more ZIPS that had data, I used the mean average of the other data points for that ZIP.
* (2) Otherwise, I used the average of that column for the whole state.
Since the point of the exercise was about finding the best thrift stores and scoring the thrift stores in a certain ZIP, this essentially removed these ZIPs with missing information from the "Best of" and "Worst of" lists and made their scores completely average. 
