# imports and setup
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import gspread

import panel as pn
pn.extension('tabulator')
import hvplot.pandas
import holoviews as hv 
hv.extension('bokeh')

# reading our data
# in my case we are using a csv locally stored
# data can also be created in our file or pulled from online
df = pd.read_csv("Discover-Last12Months.csv")

# cleaning df
df = df[['Trans. Date', 'Description', 'Amount', 'Category']] #here i am only keeping the categories i actually want to use (The only category I am eliminating is "Posted Date")
df = df.rename(columns={'Trans. Date': 'Date'}) #rename Trans. Date to Date for easier use

#***[optional cleaning]***

#df = df[df['Category'].isin(['Gasoline', 'Medical Services'])]  #This would only bring data that is labeled as Gasoline or Medical Services in the Category section - for my case we are keeping all categories present but this is an option for different use cases

# OR

#df = df[df['Amount']<=3] #This would only bring data that its total amount is less than 3

df.head()


#***[VISUALIZATIONS]***

#first visualization is a simple histogram showing how many of each transaction Category I have made in the last 12 months

sns.histplot(df['Category'])
plt.show()

#as we can see its a pretty chaotic histogram so lets actually do some more cleaning to make it easier
#i wwant to see just what ive spent most of my money on in January 2024

df2 = df[(df['Date'] > '01/01/2024') & (df['Date'] < '02/01/2024')]
sns.histplot(df2['Category'])
plt.show()

#this is easier to visualize as there isnt as much data and I can start to see my spending in January 2024, however it still isn't very easy on the eye
#lets order this chart in descending order

sns.countplot(data=df2, x='Category', order=df2['Category'].value_counts().index) #order it in descending
plt.show()

#we can see from this that most of my transactions are supermarkets, merchandise and Travel/entertainment
#now how might this compare to the amount of money spent

lastMonthTotal = df2.groupby('Category')['Amount'].sum().reset_index() #sum the total amount counted in each category
lastMonthTotal = lastMonthTotal[lastMonthTotal['Amount']>0] #only work with data that is above 0 (this removes me paying my credit bill which is -1000 roughly)
sns.barplot(x="Category", y="Amount", data=lastMonthTotal, order=lastMonthTotal.sort_values('Amount', ascending=False).Category) #create a bar plot in descending order
print(lastMonthTotal)
plt.show()

#by doing this we can see a large majority of my money spent comes from supermarkets followed by merchandise
#this suggests that I stand to save the most money by decreasing supermarket cost and merchandise cost
#lets see what percentage of last months spending was on each category - we will do a pie chart because that is better for to visualize percentages

lastMonthTotalExpenses = lastMonthTotal['Amount'].sum()
print("Last month's total expenses was: " + str(lastMonthTotalExpenses))
plt.pie(lastMonthTotal['Amount'], labels=lastMonthTotal['Category'], autopct='%.0f%%')
plt.show()

#the pie graph shows that supermarkets were 49% of my spending, merchandise was 23% and the remaining categories summed up to only be 28%
#next lets look at all my spending at supermarkets in the past 12 months and compare that to the total amount of money I have spent in that same time and see if my most recent months spending habits are similar to that of the entire past 12 months

twelveMonthTotal = df.groupby('Category')['Amount'].sum().reset_index() #sum the total amount counted in each category in past 12 months
twelveMonthTotal = twelveMonthTotal[twelveMonthTotal['Amount']>0] #only work with data that is above 0 (exclude all statements I paid off))
plt.pie(twelveMonthTotal['Amount'], labels=twelveMonthTotal['Category'], autopct='%.0f%%')
plt.show()

#we can see from this 12 month average that I usually spend 21% of my monthly bill on supermarkets, so recently something changed that caused that percentage to go up. This could be from a few reasons.
#I could be spending more money per month on supermarkets than I have in the past. Or maybe my spending in other categories has decreased and my supermarket cost stayed the same but as a result from decrease in total spending it shows as a higher percentage.
#To figure out that I can just plot my monthly supermarket bill across 12 months and see how it changes

#date column is hard to use for an entire month so lets just it from MM/DD/YYYY to Month_Year
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
#filter by Month
df['Month_Year'] = df['Date'].dt.to_period('M')
#filter rows with category Supermarkets bc thats the data we interested in
supermarket_df = df[df['Category'] == 'Supermarkets']
#group by month and sum the amounts
monthly_supermarket_spending = supermarket_df.groupby('Month_Year')['Amount'].sum().reset_index()
sns.barplot(data=monthly_supermarket_spending, x='Month_Year', y='Amount')
plt.show()

#looking at this data we see that my total supermarket bill jumped drastically starting November 2023 and continued in a high area until present date. This implies something changed from October to November that affected my spending habits.
# My assumption is because I moved from an area that is cheaper (Clemson, SC) to an area that is more expensive (Boulder, CO) however I can't say with certainty but it is something to look into in the future. My supermarket spending could've increased bc I started running more
# and thus needed more calories. We can't be absolutely certain without more data outside of this current dataset. Next we also se a large spike in spending in June. This also suggest something happened that was unique to June in my supermarket spending. I can't say with absolute certainty without
# more data however I suspect that is because it was during one of my final months on The Pacific Crest Trail and during the month of June I was averaging over 35 miles of hiking per day which meant I needed to spend more money at supermarkets to replenish my lost calories.
