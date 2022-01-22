import facebook
import ast
import pandas as pd
import requests
from sqlalchemy import create_engine

# accesing token from FACEBOOK DEVELOPER ENGINE 
token = "EAAMXH4prhKoBANHzdDT0m7WyEoAcyuan8sUhM6UN1NWA9Yt9QvmwRfIsDoQWb8gbcpkBhNcM0sNV51mVqgCnp16dh816ltuLfLueZBn1M0xcMFZBgVja3A5pNYCpDXsFXVzGAEEZBPzlDZAnZB2IaKZA7iuwhX1O6tNKpzEaOoiBi36n4M2KMJhos5fadPER7tG1abp6DBhj3grQIJBKD5" 
#making an empty list so we can append the list of id,name,created_name from the JSON for every post made by the user
b = []

graph = facebook.GraphAPI(token)
# Making a variable 
like = graph.get_object('/me/posts',fields='created_time,id,name')
a= list(like.values())

# Fisrt list of dicts is converted into a list of lists b as mentioned 10 
for i in range(len(a[0])):
    b.append(list(a[0][i].values()))

# makinga acount variable to see that how many times the api was called 
count = 0
# Acessing the next dictionary where link is posted 
c = like['paging']['next']
# making a while loop so we can get all the data posted by the user
while c[:4] == 'http':
    # getting data from link
    like1 = requests.get(c)
    # data fetched is in string so made it dict 
    like1 = ast.literal_eval(like1.text)
    # fetching the data needed
    like2 = list(like1.values())
    #dicts is converted into a list of lists b as mentioned 19 

    for i in range(len(like2[0])):
        b.append(list(like2[0][i].values()))
    try :
        # trying to see if next dict keys is there
        if (list(like1['paging'].keys()))[1] == 'next':
            # making a string for next if succeded above
            c = like1['paging']['next']
            # there is a "\\" string disturbing the link so removing it 
            c = c.replace("\\",'')
            # counting the while loop
            count = count+1
    except:
        # if no 'next' key value is there than we have 
        c = ''

# making the col list for data frame
col = a[0][0].keys()
col = list(col)
col.append('name')
print('Columns for dataframe are',col)


df = pd.DataFrame(b,columns = col)
df['created_time'] = pd.to_datetime(df['created_time']).dt.date
print('data in raw with date stamp only',df.head())

df[['NA','id']] = df['id'].str.split('_',expand = True)
print('data frame is having unique ID  ',df.head())
df = df.drop(['NA'],axis = 1) 
df= df[~df['name'].isna()]
print('data frame is having unique ID and No NULL values ',df.head())
df.to_csv (r'C:\Users\Muhammad Saad\Desktop\posts.csv', index = False, header=True)
engine = create_engine('mysql+mysqlconnector://root:Saad786b@localhost:3306/testing', echo=False)

df.to_sql(name='posts', con=engine, if_exists = 'append', index=False)