# Sv
# Homework 2

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
    print(f"Reading {filename}...")
    
    # Open and read file
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    # Extract data from each line
    first_name = lines[0].replace("First: ", "").strip()
    last_name = lines[1].replace("Last: ", "").strip()
    item = lines[2].replace("Item: ", "").strip()
    amount = lines[3].replace("Amount: ", "").strip()
    
    # Add to lists
    first_names.append(first_name)
    last_names.append(last_name)
    items.append(item)
    amounts.append(amount)
    
    print(f"  Added: {first_name} {last_name}")

# Createing DataFrame
bills_df = pd.DataFrame({
    'First': first_names,
    'Last': last_names,
    'Item': items,
    'Amount': amounts
})

# Save to CSV
bills_df.to_csv('all_bills.csv', index=False)

print("Task 1 completed!")
print(bills_df)

# TASK 2:
os.chdir('D:/adelphi/MachineLearning/homework2 data/Task 2 data/')

# Read all data files
sales_df = pd.read_csv('sales.csv')
rating1_df = pd.read_csv('customer_rating_1.csv')
rating2_df = pd.read_csv('customer_rating_2.csv')

print("Files loaded successfully")

# column name fixed 
rating2_df = rating2_df.rename(columns={'record id': 'record_id'})

# Combineing rating files
all_ratings = pd.concat([rating1_df, rating2_df], ignore_index=True)

# Merging sales with ratings
merged_df = pd.merge(sales_df, all_ratings, on='record_id', how='left')

print("Data merged successfully")

# filling columns
numerical_cols = merged_df.select_dtypes(include=['number']).columns
for col in numerical_cols:
    if merged_df[col].isnull().any():
        merged_df[col].fillna(merged_df[col].mean(), inplace=True)

categorical_cols = merged_df.select_dtypes(include=['object']).columns
for col in categorical_cols:
    if merged_df[col].isnull().any():
        merged_df[col].fillna(merged_df[col].mode()[0], inplace=True)

print("Missing values handled")

# Creating new columns
# 1 Sales rating 
rating_cols = ['Service_Rating', 'Sales_Rep_Rating', 'Product_Rating']
merged_df['Sales_Rating'] = merged_df[rating_cols].mean(axis=1)

# 2 Profit raniking and profit ranking
merged_df['Profit'] = merged_df['Sales'] - merged_df['COGS']

def categorize_profit(profit):
    if profit < 500:
        return 'Small Profit'
    elif profit <= 2000:
        return 'Medium Profit'
    else:
        return 'Large Profit'

merged_df['Profit_Rank'] = merged_df['Profit'].apply(categorize_profit)

print("New columns created")

# Generate statistics
basic_stats = merged_df.describe()
numerical_data = merged_df.select_dtypes(include=['number'])
detailed_stats = numerical_data.agg(['mean', 'min', 'max', 'std'])
# Save all results
merged_df.to_csv('processed_sales_data.csv', index=False)
basic_stats.to_csv('basic_statistics.csv')
detailed_stats.to_csv('detailed_statistics.csv')

print("Task 2 completed!")
# Show final result
print("\nFirst 5 rows of processed data:")
print(merged_df.head())