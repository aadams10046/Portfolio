# Data Analyst Portfolio
This ongoing project is meant to create a search function allowing the user to search the ZIP code of a thrift store and see the percentile scores of four categories of thrift shopping in that ZIP code. Also visualizations of demographics information are presented.

## Technical Skills Utilized
* Python
* Data Visualization using matplotlib, and seaborn (examples in files) 
* Data analysis using pandas, numpy, and scipy.stats.
* Excel formulas and references (for creating the csv that the program uses)
* Tableau Income and Age Maps available [here](https://public.tableau.com/app/profile/alexander.adams3449/viz/MichiganMaps/Income).

## Process
The data used for the initial .csv was pulled from Census.gov data collected in 2020. Some ZIP codes had no data collected for income or median age. In these cases I did one of two things: 
1. If a city had two or more ZIPS that had data, I used the mean average of the other data points for that ZIP.
2. Otherwise, I used the average of that column for the whole state.
Since the point of the exercise was about finding the best thrift stores and scoring the thrift stores in a certain ZIP, this essentially removed these ZIPs with missing information from the "Best of" and "Worst of" lists and made their scores completely average. 

I then used [APIFY's Google Maps Scraper] (https://console.apify.com/) to pull the list of all thrift stores and clothes resale shops in Michigan. I used all of this generated information to generate the count of all thrift stores after cleaning the scraper-generated data.
Once this was complete I used SQL to join the business count and master list data. Once complete, I used this information to build the Tableau vizualizations linked above.

## Full SQL Code Below
```SQL
CREATE TABLE "Full_Thrift_Store_List" (
	"postal_code"	INTEGER,
	"address"	TEXT,
	"category_name"	TEXT,
	"city"	TEXT,
	"latitude"	REAL,
	"longitude"	REAL,
	"neighborhood"	TEXT,
	"permanently_closed"	TEXT,
	"phone"	TEXT,
	"state"	TEXT,
	"temporarily_closed"	TEXT,
	"title"	TEXT,
	"total_score"	REAL,
	"website"	TEXT
)

CREATE TABLE "master_thrift_store" (
	"Name"	TEXT,
	"ZIP"	INTEGER,
	"Median_Income"	INTEGER,
	"Median_Age"	INTEGER,
	"Median_Male_Age"	INTEGER,
	"Median_Female_Age"	INTEGER
)

--Clean Out any non-Michigan ZIPs: There apparently are none

SELECT * FROM Full_Thrift_Store_List
WHERE postal_code NOT BETWEEN 48001 AND 49971;

--Check for and clean out any permanently closed businesses: 24 businesses found and deleted
SELECT * FROM Full_Thrift_Store_List
WHERE permanently_closed = 'TRUE' OR temporarily_closed = 'TRUE';

DELETE FROM Full_Thrift_Store_List WHERE permanently_closed = 'TRUE'  OR temporarily_closed = 'TRUE';

--Look at list of unique business types
SELECT DISTINCT(category_name) AS 'Unique Categories List'  FROM Full_Thrift_Store_List;

--Check for and clean out any non-thrift stores: removed 1005 businesses
SELECT * FROM Full_Thrift_Store_List
WHERE category_name NOT IN ('Thrift store', 'Charity', 'Second hand store', 'Non-profit organization', 'Donations center', 'Used clothing store', 'Clothes market') OR category_name IS NULL;

DELETE FROM Full_Thrift_Store_List 
WHERE category_name NOT IN ('Thrift store', 'Charity', 'Second hand store', 'Non-profit organization', 'Donations center', 'Used clothing store', 'Clothes market') OR category_name IS NULL;

--Clean data so that all state codes are 'MI'
SELECT COUNT(*) AS 'Count of MI State Code' FROM Full_Thrift_Store_List WHERE state <> 'MI'

UPDATE Full_Thrift_Store_List
SET state = CASE
	WHEN state <> 'MI' THEN 'MI'
END

--Count all businesses by ZIP and join that table to Master List for use in Data_Boy.py
SELECT postal_code,
COUNT(*) AS Business_Count
FROM Full_Thrift_Store_List
GROUP BY 1
ORDER BY 2 DESC;

CREATE TABLE "Business_Count_by_ZIP" (
	"postal_code"	INTEGER,
	"Business_Count"	INTEGER
)

--JOIN business count and ZIP list on ID ZIP
SELECT master_thrift_store.*,  Business_Count_by_ZIP.*
FROM master_thrift_store
JOIN Business_Count_by_ZIP
ON master_thrift_store.ZIP = Business_Count_by_ZIP.postal_code
ORDER BY ZIP;
```

## Full Python Code Below
```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats as st

#Reading csv and using it to create dictionary of all entries
master = pd.read_csv('master_thrift_store.csv')
master_dict = master.to_dict()


#Finding Max and Min Median_Income Values and associated indices in dictionary
max_median_income = max(master_dict['Median_Income'].values())
max_median_income_city = master_dict.get('Name').get(list(master_dict['Median_Income'].values()).index(max_median_income))
max_median_income_zip = master_dict.get('ZIP').get(list(master_dict['Median_Income'].values()).index(max_median_income))
min_median_income = min(master_dict['Median_Income'].values())
min_median_income_city = master_dict.get('Name').get(list(master_dict['Median_Income'].values()).index(min_median_income))
min_median_income_zip = master_dict.get('ZIP').get(list(master_dict['Median_Income'].values()).index(min_median_income))

#Repeating Process above for Median_Age
max_median_age = max(master_dict['Median_Age'].values())
min_median_age = min(master_dict['Median_Age'].values())
max_median_age_city = master_dict.get('Name').get(list(master_dict['Median_Age'].values()).index(max_median_age))
min_median_age_city = master_dict.get('Name').get(list(master_dict['Median_Age'].values()).index(min_median_age))
max_median_age_zip = master_dict.get('ZIP').get(list(master_dict['Median_Age'].values()).index(max_median_age))
min_median_age_zip = master_dict.get('ZIP').get(list(master_dict['Median_Age'].values()).index(min_median_age))

#Finding given zip's percentile for health score
your_zip = int(input("Enter ZIP:"))
income_by_zip = master_dict.get('Median_Income').get(list(master_dict['ZIP'].values()).index(your_zip))
age_by_zip = master_dict.get('Median_Age').get(list(master_dict['ZIP'].values()).index(your_zip))
m_age_by_zip = master_dict.get('Median_Male_Age').get(list(master_dict['ZIP'].values()).index(your_zip))
f_age_by_zip = master_dict.get('Median_Female_Age').get(list(master_dict['ZIP'].values()).index(your_zip))

#Creating Health Score (all scores out of 100)
health = {'Vintage': st.percentileofscore(master['Median_Age'], age_by_zip), "Men's Vintage": st.percentileofscore(master['Median_Male_Age'], m_age_by_zip), "Women's Vintage": st.percentileofscore(master['Median_Female_Age'], f_age_by_zip), "Name Brand": st.percentileofscore(master['Median_Income'], income_by_zip)}

print("***Scores out of 100***\nVintage Score: {}\nMen's Vintage Score:{}\nWomen's Vintage Score:{}\nName Brand Score:{}\n\n".format(round(health.get("Vintage"),0), round(health.get("Men's Vintage"),0), round(health.get("Women's Vintage"),0), round(health.get("Name Brand"),0)))

#Plotting Age v. Income data
plt.scatter(master_dict['Median_Age'].values(),master_dict['Median_Income'].values(),marker = "D", alpha = 0.5)
plt.xlabel("Median Age")
plt.ylabel("Median Income (USD)")
plt.title("Age vs. Income in Michigan")
plt.show()

#Creating distribution graphs for median income
plt.hist(master_dict['Median_Income'].values(), bins=25, edgecolor="white", color='green')
plt.xlabel("Median Income")
plt.ylabel("Count")
plt.title("Median Income Histogram")
plt.show()

#Creating distribution graphs for median income
plt.hist(master_dict['Median_Age'].values(), bins=10, edgecolor="white", color='gray')
plt.xlabel("Median Age")
plt.ylabel("Count")
plt.title("Median Age Histogram")
plt.show()

#Plotting the same data with regression line and confidence interval bands in seaborn
df = pd.DataFrame(master,columns = ['Median_Age','Median_Income'])
sns.regplot(data = df, x = 'Median_Age', y = 'Median_Income', scatter_kws = {'color':'blue', 'alpha':0.5}, line_kws = {'color':'red'})
plt.show()

#Creating Best of List and printing it
master = master.sort_values(['Median_Age'],axis = 0, ascending = [False], inplace = False)
print('Top 5 Vintage Shopping Locations:\n(1){} {}\n(2){} {}\n(3){} {}\n(4){} {}\n(5){} {}\n\n'.format(max_median_age_city, max_median_age_zip, master.iat[1,0], master.iat[1,1], master.iat[2,0], master.iat[2,1], master.iat[3,0], master.iat[3,1], master.iat[4,0], master.iat[4,1], master.iat[5,0], master.iat[5,1]))
master = master.sort_values(['Median_Income'], axis = 0, ascending = [False], inplace = False)
print('Top 5 Luxury Brand Shopping Locations:\n(1){} {}\n(2){} {}\n(3){} {}\n(4){} {}\n(5){} {}\n\n'.format(max_median_income_city, max_median_income_zip, master.iat[1,0], master.iat[1,1], master.iat[2,0], master.iat[2,1], master.iat[3,0], master.iat[3,1], master.iat[4,0], master.iat[4,1], master.iat[5,0], master.iat[5,1]))
master = master.sort_values(['Median_Male_Age'], axis = 0, ascending = [False], inplace = False)
print("Top 5 Men's Vintage Shopping Locations:\n(1){} {}\n(2){} {}\n(3){} {}\n(4){} {}\n(5){} {}\n\n".format(master.iat[0,0], master.iat[0,1], master.iat[1,0], master.iat[1,1], master.iat[2,0], master.iat[2,1], master.iat[3,0], master.iat[3,1], master.iat[4,0], master.iat[4,1], master.iat[5,0], master.iat[5,1]))
master = master.sort_values(['Median_Female_Age'], axis = 0, ascending = [False], inplace = False)
print("Top 5 Women's Vintage Shopping Locations:\n(1){} {}\n(2){} {}\n(3){} {}\n(4){} {}\n(5){} {}\n\n".format(master.iat[0,0], master.iat[0,1], master.iat[1,0], master.iat[1,1], master.iat[2,0], master.iat[2,1], master.iat[3,0], master.iat[3,1], master.iat[4,0], master.iat[4,1], master.iat[5,0], master.iat[5,1]))

#Creating Worst of List and printing it
master = master.sort_values(['Median_Age'],axis = 0, ascending = [True], inplace = False)
print('Top 5 Vintage Shopping Locations:\n(1){} {}\n(2){} {}\n(3){} {}\n(4){} {}\n(5){} {}\n\n'.format(max_median_age_city, max_median_age_zip, master.iat[1,0], master.iat[1,1], master.iat[2,0], master.iat[2,1], master.iat[3,0], master.iat[3,1], master.iat[4,0], master.iat[4,1], master.iat[5,0], master.iat[5,1]))
master = master.sort_values(['Median_Income'], axis = 0, ascending = [True], inplace = False)
print('Top 5 Luxury Brand Shopping Locations:\n(1){} {}\n(2){} {}\n(3){} {}\n(4){} {}\n(5){} {}\n\n'.format(max_median_income_city, max_median_income_zip, master.iat[1,0], master.iat[1,1], master.iat[2,0], master.iat[2,1], master.iat[3,0], master.iat[3,1], master.iat[4,0], master.iat[4,1], master.iat[5,0], master.iat[5,1]))
master = master.sort_values(['Median_Male_Age'], axis = 0, ascending = [True], inplace = False)
print("Top 5 Men's Vintage Shopping Locations:\n(1){} {}\n(2){} {}\n(3){} {}\n(4){} {}\n(5){} {}\n\n".format(master.iat[0,0], master.iat[0,1], master.iat[1,0], master.iat[1,1], master.iat[2,0], master.iat[2,1], master.iat[3,0], master.iat[3,1], master.iat[4,0], master.iat[4,1], master.iat[5,0], master.iat[5,1]))
master = master.sort_values(['Median_Female_Age'], axis = 0, ascending = [True], inplace = False)
print("Top 5 Women's Vintage Shopping Locations:\n(1){} {}\n(2){} {}\n(3){} {}\n(4){} {}\n(5){} {}\n\n".format(master.iat[0,0], master.iat[0,1], master.iat[1,0], master.iat[1,1], master.iat[2,0], master.iat[2,1], master.iat[3,0], master.iat[3,1], master.iat[4,0], master.iat[4,1], master.iat[5,0], master.iat[5,1]))
```
