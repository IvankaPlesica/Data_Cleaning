#!/usr/bin/env python
# coding: utf-8
# This is a collection of a few common cleaning functions that usually come in handy.
# The exercises were done mostly following an existing exercise online.

import pandas as pd

df = pd.read_excel(r"C:\Users\ivank\Downloads\Customer Call List.xlsx")

#This line deletes duplicate values.
df = df.drop_duplicates()

#Removes a whole column that isn't useful.
df = df.drop(columns = "Not_Useful_Column")


#Different iterations of the strip function, used depending on investigating data.
df["Last_Name"] = df["Last_Name"].str.lstrip("...")
df["Last_Name"] = df["Last_Name"].str.lstrip("/")
df["Last_Name"] = df["Last_Name"].str.rstrip("_")
df["Last_Name"] = df["Last_Name"].str.lstrip("123._/")

#str.replace is being used to remove specific caracters by replacing them with ''.
#lamdba function is being used to standardize formats; useful when we need to apply a function to a single column.
df["Phone_Number"]=df["Phone_Number"].str.replace('[^a-zA-Z0-9]','')
df["Phone_Number"] = df["Phone_Number"].apply(lambda x: str(x))
df["Phone_Number"] = df["Phone_Number"].apply(lambda x: x[0:3] + '-' + x[3:6] + '-' + x[6:10])
df["Phone_Number"] = df["Phone_Number"].str.replace('nan--','').replace('na--','').replace('Na--','')

#Standard approach to separating an address into separate columns, based on different elements of an address.
df[["Street_Address", "State", "Zip_Code"]] = df["Address"].str.split(',',2,expand = True)

#Setting regex to False so it treats 'Y' literally and not as a regular expression pattern.
df["Paying Customer"] = df["Paying Customer"].replace('Y', 'Yes', regex = False).replace('N', 'No')
df["Do_Not_Contact"] = df["Do_Not_Contact"].replace('Y', 'Yes', regex = False).replace('N', 'No', regex = False)

#Different ways of replacing missing values with an empty string
df["Paying Customer"] = df["Paying Customer"].replace('N/a', '', regex = False)
df["Do_Not_Contact"] = df["Do_Not_Contact"].replace('N/a', '', regex = False)
df = df.fillna('')


#Creating a new data frame based on an importan condition. Here, it separates customers based on their permission
#to use ther given phone numbers
df_call_list = df[(df["Do_Not_Contact"]  == 'No') & (df["Phone_Number"] != '')]


#Since drop usually operates on rows, we use axis to drop columns.
df_call_list.reset_index(drop = True)
df_call_list = df_call_list.drop("Address", axis = 1)
df = df.drop("Address", axis = 1)
df_call_list


# # FIFA DATASET - a little exercise

# ### Insert and inspect data; remove duplicates

df = pd.read_csv(r"C:\Users\ivank\Downloads\archive\fifa21 raw data v2.csv")
df.drop_duplicates()


# ### Club
df["Club"] = df["Club"].replace(r'\s+|\\n', '', regex = True)


pd.set_option('display.max_columns', None)

#Cleaning strings in data.
df["Club"] = df["Club"].str.strip()
df["Club"] = df["Club"].replace('FC', ' FC ', regex = True)
df["Club"] = df["Club"].str.findall('[A-Z]*[^A-Z]*')
df["Club"] = df["Club"].str.join(" ")
df["Club"] = df["Club"].replace("- ", "-", regex = True)
df["Club"] = df["Club"].str.strip()


# ### Value
#unifying value data types
df["Value"] = df["Value"].str.lstrip('€')
df["Value"] = df["Value"].astype(float)
df["Value M/K"] = df["Value M/K"].astype(float)

df_value.unique()
df_value = df["Value"].str[-1].replace('M', 1000000).replace('K', 1000)


df["Value"] = df["Value"].str.rstrip('K')
df["Value"] = df["Value"].str.rstrip('M')


df["Value"].astype(float).multiply(df_value, axis = 0)
df["Value"] = (df["Value"] * df["Value M/K"]).astype(int)


# ### Wage
#removing symbols from a wage to make it usable for calculations
df["Wage"] = df["Wage"].str.lstrip('€')
df["Wage"].unique()

#making the values usable for calculations
df["Wage"] = df["Wage"].replace("K", "000", regex = True)
df["Wage"] = df["Wage"].astype(int)


# ### Release Clause

df["Release Clause"] = df["Release Clause"].str.lstrip('€')
df["Release Clause"].unique()


