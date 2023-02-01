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


#Function for finding given zip's percentile for health score and printing it
def health_scorer():
    your_zip = int(input("Enter ZIP:"))
    income_by_zip = master_dict.get('Median_Income').get(list(master_dict['ZIP'].values()).index(your_zip))
    age_by_zip = master_dict.get('Median_Age').get(list(master_dict['ZIP'].values()).index(your_zip))
    m_age_by_zip = master_dict.get('Median_Male_Age').get(list(master_dict['ZIP'].values()).index(your_zip))
    f_age_by_zip = master_dict.get('Median_Female_Age').get(list(master_dict['ZIP'].values()).index(your_zip))
    #Creating Health Score (all scores out of 100)
    health = {'Vintage': st.percentileofscore(master['Median_Age'], age_by_zip), "Men's Vintage": st.percentileofscore(master['Median_Male_Age'], m_age_by_zip), "Women's Vintage": st.percentileofscore(master['Median_Female_Age'], f_age_by_zip), "Name Brand": st.percentileofscore(master['Median_Income'], income_by_zip)}
    print("\n***Scores out of 100***\nVintage Score: {}\nMen's Vintage Score:{}\nWomen's Vintage Score:{}\nName Brand Score:{}\n\n".format(round(health.get("Vintage"),0), round(health.get("Men's Vintage"),0), round(health.get("Women's Vintage"),0), round(health.get("Name Brand"),0)))

#Function for plotting Age v. Income data
def age_v_income():
    plt.scatter(master_dict['Median_Age'].values(),master_dict['Median_Income'].values(),marker = "D", alpha = 0.5)
    plt.xlabel("Median Age")
    plt.ylabel("Median Income (USD)")
    plt.title("Age vs. Income in Michigan")
    plt.show()

#Function for creating distribution graphs for median income
def graph_med_income():
    plt.hist(master_dict['Median_Income'].values(), bins=25, edgecolor="white", color='green')
    plt.xlabel("Median Income")
    plt.ylabel("Count")
    plt.title("Median Income Histogram")
    plt.show()

#Function for creating distribution graphs for median age
def graph_med_age():
    plt.hist(master_dict['Median_Age'].values(), bins=10, edgecolor="white", color='gray')
    plt.xlabel("Median Age")
    plt.ylabel("Count")
    plt.title("Median Age Histogram")
    plt.show()

#Function for plotting the same data with regression line and confidence interval bands in seaborn
def graph_med_age_sns():
    df = pd.DataFrame(master,columns = ['Median_Age','Median_Income'])
    sns.regplot(data = df, x = 'Median_Age', y = 'Median_Income', scatter_kws = {'color':'blue', 'alpha':0.5}, line_kws = {'color':'red'})
    plt.xlabel("Median Age")
    plt.ylabel("Count")
    plt.title("Median Age Histogram")
    plt.show()

#Function for creating Best of List and printing it
def best_of(characteristic):
    characteristic = characteristic.lower()
    if characteristic == 'vintage':
        master = master.sort_values(['Median_Age'],axis = 0, ascending = [False], inplace = False)
        print(f'Top 5 Vintage Shopping Locations:\n(1){max_median_age_city} {max_median_age_zip}\n(2){master.iat[1,0]} {master.iat[1,1]}\n(3){master.iat[2,0]} {master.iat[2,1]}\n(4){master.iat[3,0]} {master.iat[3,1]}\n(5){master.iat[4,0]} {master.iat[4,1]}\n\n')
    #Above I use f strings to create the print statement, while using .format below. This is because I think the f string syntax actually hampers the readability in this case.
    elif characteristic == 'luxury':
        master = master.sort_values(['Median_Income'], axis = 0, ascending = [False], inplace = False)
        print('Top 5 Luxury Brand Shopping Locations:\n(1){} {}\n(2){} {}\n(3){} {}\n(4){} {}\n(5){} {}\n\n'.format(max_median_income_city, max_median_income_zip, master.iat[1,0], master.iat[1,1], master.iat[2,0], master.iat[2,1], master.iat[3,0], master.iat[3,1], master.iat[4,0], master.iat[4,1]))
    elif characteristic == 'mens':
        master = master.sort_values(['Median_Male_Age'], axis = 0, ascending = [False], inplace = False)
        print("Top 5 Men's Vintage Shopping Locations:\n(1){} {}\n(2){} {}\n(3){} {}\n(4){} {}\n(5){} {}\n\n".format(master.iat[0,0], master.iat[0,1], master.iat[1,0], master.iat[1,1], master.iat[2,0], master.iat[2,1], master.iat[3,0], master.iat[3,1], master.iat[4,0], master.iat[4,1]))
    elif characteristic == 'womens':
        master = master.sort_values(['Median_Female_Age'], axis = 0, ascending = [False], inplace = False)
        print("Top 5 Women's Vintage Shopping Locations:\n(1){} {}\n(2){} {}\n(3){} {}\n(4){} {}\n(5){} {}\n\n".format(master.iat[0,0], master.iat[0,1], master.iat[1,0], master.iat[1,1], master.iat[2,0], master.iat[2,1], master.iat[3,0], master.iat[3,1], master.iat[4,0], master.iat[4,1]))
    else:
        print(f'{characteristic} is not a choice from the list.\nPlease try again.')

#Function for creating Worst of List and printing it
def worst_of(characteristic):
    characteristic = characteristic.lower()
    if characteristic == 'vintage':
        master = master.sort_values(['Median_Age'],axis = 0, ascending = [True], inplace = False)
        print('Top 5 Vintage Shopping Locations:\n(1){} {}\n(2){} {}\n(3){} {}\n(4){} {}\n(5){} {}\n\n'.format(max_median_age_city, max_median_age_zip, master.iat[1,0], master.iat[1,1], master.iat[2,0], master.iat[2,1], master.iat[3,0], master.iat[3,1], master.iat[4,0], master.iat[4,1]))
    elif characteristic == 'luxury':
        master = master.sort_values(['Median_Income'], axis = 0, ascending = [True], inplace = False)
        print('Top 5 Luxury Brand Shopping Locations:\n(1){} {}\n(2){} {}\n(3){} {}\n(4){} {}\n(5){} {}\n\n'.format(max_median_income_city, max_median_income_zip, master.iat[1,0], master.iat[1,1], master.iat[2,0], master.iat[2,1], master.iat[3,0], master.iat[3,1], master.iat[4,0], master.iat[4,1]))
    elif characteristic == 'mens':
        master = master.sort_values(['Median_Male_Age'], axis = 0, ascending = [True], inplace = False)
        print("Top 5 Men's Vintage Shopping Locations:\n(1){} {}\n(2){} {}\n(3){} {}\n(4){} {}\n(5){} {}\n\n".format(master.iat[0,0], master.iat[0,1], master.iat[1,0], master.iat[1,1], master.iat[2,0], master.iat[2,1], master.iat[3,0], master.iat[3,1], master.iat[4,0], master.iat[4,1]))
    elif characteristic == 'womens':
        master = master.sort_values(['Median_Female_Age'], axis = 0, ascending = [True], inplace = False)
        print("Top 5 Women's Vintage Shopping Locations:\n(1){} {}\n(2){} {}\n(3){} {}\n(4){} {}\n(5){} {}\n\n".format(master.iat[0,0], master.iat[0,1], master.iat[1,0], master.iat[1,1], master.iat[2,0], master.iat[2,1], master.iat[3,0], master.iat[3,1], master.iat[4,0], master.iat[4,1]))
    else:
        print(f'{characteristic} is not a choice from the list.\nPlease try again.')
