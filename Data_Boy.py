import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import decimal as d
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

#Creating Health Score
health = {'Vintage': st.percentileofscore(master['Median_Age'], age_by_zip), "Men's Vintage": st.percentileofscore(master['Median_Male_Age'], m_age_by_zip), "Women's Vintage": st.percentileofscore(master['Median_Female_Age'], f_age_by_zip), "Name Brand": st.percentileofscore(master['Median_Income'], income_by_zip)}

print("Vintage Score: {}\nMen's Vintage Score:{}\nWomen's Vintage Score:{}\nBrand Name Score:{}".format(health.get("Vintage"), health.get("Men's Vintage"), health.get("Women's Vintage"), health.get("Brand Name")))

#Plotting Age v. Income data (This is unrelated to the project above, I was just curious about the relationship.)
plt.scatter(master_dict['Median_Age'].values(),master_dict['Median_Income'].values(),marker = "D", alpha = 0.5)
plt.xlabel("Median Age")
plt.ylabel("Median Income (USD)")
plt.title("Age vs. Income in Michigan")
plt.show()
