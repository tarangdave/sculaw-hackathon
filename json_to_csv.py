import sys
import pandas as pd
from pandas import DataFrame
import json
from pandas.io.json import json_normalize


data=r'criminal.json'

# Reads and converts json to dict.
def js_r(data):
   with open(data, encoding='utf-8') as f_in:
       return(json.load(f_in))

my_data = js_r(data)
df = json_normalize(my_data['record'],'Charges',['Name','Role','Case Number','Filing Date', 'Status', 'Status Date'])

df.to_csv('criminal.csv')




# if __name__ == "__main__":
#     my_dic_data = js_r(data)
#     print("This is my dictionary", my_dic_data)
# keys= my_dic_data.keys()
# print ("The original dict keys",keys)
# # You assign a new dictionary key- SO_users, and make dictionary comprehension = { your_key: old_dict[your_key] for your_key in your_keys }
# dict_you_want={'my_items':my_dic_data['record']['Charges']for key in keys}

# print ("These are the keys to dict_you_want",dict_you_want.keys())


# print ("This is the dictionary of SO_users", dict_you_want)
# df=pd.DataFrame(dict_you_want)
# print ("df:", df)
# #When .apply(pd.Series) method on items column is applied, the dictionaries in items column will be used as column headings
# df2=df['my_items'].apply(pd.Series)
# print ("df2",df2)
# df3=pd.concat([df2.drop(['user'],axis=1),df2['user'].apply(pd.Series)],axis=1)
# #df3=df2['user'].apply(pd.Series)

# print ("df3",df3)