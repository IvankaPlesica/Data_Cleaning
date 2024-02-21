#!/usr/bin/env python
# coding: utf-8

# In[110]:


import pandas as pd


# In[3]:


df = pd.read_excel(r"C:\Users\ivank\Downloads\Customer Call List.xlsx")
df


# In[6]:


df = df.drop_duplicates()
df


# In[8]:


df = df.drop(columns = "Not_Useful_Column")


# In[15]:


df["Last_Name"] = df["Last_Name"].str.lstrip("...")
df["Last_Name"] = df["Last_Name"].str.lstrip("/")
df["Last_Name"] = df["Last_Name"].str.rstrip("_")
#df["Last_Name"] = df["Last_Name"].str.lstrip("123._/")
df


# In[14]:


df


# In[28]:


#df["Phone_Number"]=df["Phone_Number"].str.replace('[^a-zA-Z0-9]','')
#df["Phone_Number"] = df["Phone_Number"].apply(lambda x: str(x))
#df["Phone_Number"] = df["Phone_Number"].apply(lambda x: x[0:3] + '-' + x[3:6] + '-' + x[6:10])
df["Phone_Number"] = df["Phone_Number"].str.replace('nan--','').replace('na--','').replace('Na--','')


# In[34]:


df[["Street_Address", "State", "Zip_Code"]] = df["Address"].str.split(',',2,expand = True)


# In[55]:


df["Paying Customer"] = df["Paying Customer"].replace('Y', 'Yes', regex = False).replace('N', 'No')


# In[58]:


df["Do_Not_Contact"] = df["Do_Not_Contact"].replace('Y', 'Yes', regex = False).replace('N', 'No', regex = False)


# In[59]:


df


# In[73]:


#df["Paying Customer"] = df["Paying Customer"].replace('N/a', '', regex = False)
#df["Do_Not_Contact"] = df["Do_Not_Contact"].replace('N/a', '', regex = False)
df = df.fillna('')


# In[74]:


df


# In[98]:


df_call_list = df[(df["Do_Not_Contact"]  == 'No') & (df["Phone_Number"] != '')]


# In[106]:


#df_call_list.reset_index(drop = True)
#df_call_list = df_call_list.drop("Address", axis = 1)
#df = df.drop("Address", axis = 1)
df_call_list


# # FIFA DATASET

# ### Insert and inspect data; remove duplicates

# In[162]:


df = pd.read_csv(r"C:\Users\ivank\Downloads\archive\fifa21 raw data v2.csv")


# In[163]:


df.head(5)


# In[164]:


df.drop_duplicates()


# ### Club

# In[165]:


df["Club"] = df["Club"].replace(r'\s+|\\n', '', regex = True)


# In[166]:


#pd.set_option('display.max_columns', None)


# In[316]:


#df["Club"] = df["Club"].str.strip()
#df["Club"] = df["Club"].replace('FC', ' FC ', regex = True)
#df["Club"] = df["Club"].str.findall('[A-Z]*[^A-Z]*')
#df["Club"] = df["Club"].str.join(" ")
#df["Club"] = df["Club"].replace("- ", "-", regex = True)
#df["Club"] = df["Club"].str.strip()
df.head(50)


# ### Value

# In[241]:


#df["Value"] = df["Value"].str.lstrip('€')
#df["Value"] = df["Value"].astype(float)
df["Value M/K"] = df["Value M/K"].astype(float)


# In[169]:


#df_value.unique()
df_value = df["Value"].str[-1].replace('M', 1000000).replace('K', 1000)


# In[180]:


df["Value"] = df["Value"].str.rstrip('K')
df["Value"] = df["Value"].str.rstrip('M')


# In[244]:


#df["Value"].astype(float).multiply(df_value, axis = 0)
df["Value"] = (df["Value"] * df["Value M/K"]).astype(int)


# In[245]:


df


# In[246]:


df["Value"]


# ### Wage

# In[318]:


df["Wage"] = df["Wage"].str.lstrip('€')


# In[320]:


df["Wage"].unique()


# In[326]:


#df["Wage"] = df["Wage"].replace("K", "000", regex = True)
df["Wage"] = df["Wage"].astype(int)


# In[328]:


df["Wage"].unique()


# ### Release Clause

# In[331]:


df["Release Clause"] = df["Release Clause"].str.lstrip('€')


# In[335]:


df["Release Clause"].unique()


# In[ ]:





# In[317]:


df["Value"]

