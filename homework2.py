# Sv
# Homework 2
#for data table 
import pandas as pd
import os

# TASK 1
os.chdir('D:/adelphi/MachineLearning/homework2 data/Task 1 data/')

# empty lists to store data
first_names = []
last_names = []
items = []
amounts = []

# Read each bill file
for i in range(1, 5):
    filename = f"Bill{i}.txt"
   
    # Open and read file
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    # Extract data from each line
    first_name = lines[0].replace("First: ", "").strip()
    last_name = lines[1].replace("Last: ", "").strip()
    item = lines[2].replace("Item: ", "").strip()
    amount = lines[3].replace("Amount: ", "").strip()
    
    # Adding info to lists
    first_names.append(first_name)
    last_names.append(last_name)
    items.append(item)
    amounts.append(amount)
    
    print("  Added: {first_name} {last_name}")

# Createing DataFrames
bills_data = pd.DataFrame({
    'First': first_names,
    'Last': last_names,
    'Item': items,
    'Amount': amounts
})

# Save to  new CSV
bills_data.to_csv('all_bills.csv', index=False)

print("Task 1 completed!")
print(bills_data)

# TASK 2:
os.chdir('D:/adelphi/MachineLearning/homework2 data/Task 2 data/')

# Read all data files
sales = pd.read_csv('sales.csv')
rating1 = pd.read_csv('customer_rating_1.csv')
rating2 = pd.read_csv('customer_rating_2.csv')

# fixing column name 
rating2 = rating2.rename(columns={'record id': 'record_id'})

# Combineing rating files
all_ratings = pd.concat([rating1, rating2], ignore_index=True)

# Merging sales with ratings
combineddata = pd.merge(sales, all_ratings, on='record_id', how='left')

# filling columns
numerical_cols = combineddata.select_dtypes(include=['number']).columns
for col in numerical_cols:
    if combineddata[col].isnull().any():
        combineddata[col].fillna(combineddata[col].mean(), inplace=True)

categorical_cols = combineddata.select_dtypes(include=['object']).columns
for col in categorical_cols:
    if combineddata[col].isnull().any():
        combineddata[col].fillna(combineddata[col].mode()[0], inplace=True)

# Creating new columns for Sales rating 
rating_cols = ['Service_Rating', 'Sales_Rep_Rating', 'Product_Rating']
combineddata['Sales_Rating'] = combineddata[rating_cols].mean(axis=1)

# creating column for Profit raniking and profit ranking
combineddata['Profit'] = combineddata['Sales'] - combineddata['COGS']

def categorize_profit(profit):
    if profit < 500:
        return 'Small Profit'
    elif profit <= 2000:
        return 'Medium Profit'
    else:
        return 'Large Profit'

combineddata['Profit_Rank'] = combineddata['Profit'].apply(categorize_profit)

# Generate statistics
basic_stats = combineddata.describe()
numerical_data = combineddata.select_dtypes(include=['number'])
detailed_stats = numerical_data.agg(['mean', 'min', 'max', 'std'])
# Save all results
combineddata.to_csv('processed_sales_data.csv', index=False)
basic_stats.to_csv('basic_statistics.csv')
detailed_stats.to_csv('detailed_statistics.csv')

print("Task 2 completed!")
print("First 5 rows of processed data:")
print(combineddata.head())
