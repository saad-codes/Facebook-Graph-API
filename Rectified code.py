import facebook
from numpy import ones_like
from sqlalchemy import (create_engine, MetaData, Table, Column, String)
meta_data = MetaData()

# accesing token from FACEBOOK DEVELOPER ENGINE 
token = "EAAXUDaw917sBABnrthOPr7Mnx3zVlBOGQ2c6sc0Ij7L1nhw5dqvpZC7hjbmnZBUyubfwdQZBQMT4eDV43UnGurqGioAAdJ8rsvxUGeLJW4zBSWyiua8FUqWnVqqqMCesx60yhZBD6tG4kVZAQGNETmQfexP4n6BlFclmyVEe4sjDtSsZC9MgJAtBbHNVOkNAxIxFxgZAYZAIWthrDXhTPQGBOZCvx4HhckqiYLpJ7cMIQ46aktUqEGjJky7LqiRhWiUAZD" 
graph = facebook.GraphAPI(token)
# Creating engine and connecting Database

engine = create_engine('mysql+mysqlconnector://root:Saad786b@localhost:3306/testing', echo=False)


# Makingg table for users
users = Table('users', meta_data,
              Column('user_id', String(100), primary_key = True),
              Column('username', String(150), nullable = False, unique = True),
              Column('email', String(150), nullable = False),
              Column('location', String(250), nullable = True),
              Column('hometown', String(250), nullable = True),
             )
posts = Table('posts', meta_data,
              Column('user_id', String(100)),
              Column('post_id', String(250), nullable = False, unique = False),
              Column('post_name', String(150)),
              Column('post_date_time', String(250), nullable = True),
             )

likes = Table('likes', meta_data,
              Column('user_id', String(100)),
              Column('page_id', String(250), nullable = False, unique = False),
              Column('page_name', String(150)),
              Column('like_date_time', String(250), nullable = True),
             )
# Connecting Data Base 

try:

  conn = engine.connect()

  print('db connected')

  print('connection object is :{}'.format(conn))

except: 

  print('db not connected')
meta_data.create_all(engine)
user_info = graph.get_object('/me',fields='id,name,gender,location,hometown,email')
def user_table():    
    ins = users.insert().values(
        user_id =  user_info['id'],
        username = user_info['name'],
        location =  user_info['location']['name'],
        hometown =  user_info['hometown']['name'],
        email = user_info['email']
    )
    print(str(ins))

    print(ins.compile().params)

    result = conn.execute(ins)

    print('Last inserted key:')

    print(result.inserted_primary_key)

user_table()


post_info = graph.get_object('/me/posts',fields='id,name,created_time')


for one_post in post_info['data']:
    k = one_post['id'].split('_')
    def post_name():
        try:
            return one_post['name']
        except:
            return 'No_Name'
        
    ins = posts.insert().values(
        user_id = user_info['id'],
        post_name = post_name(),
        post_id =  k[0],
        post_date_time = one_post['created_time']
    )
    print(str(ins))

    print(ins.compile().params)

    result = conn.execute(ins)

    print('Last inserted key:')

    print(result.inserted_primary_key)

    
    
    

like_info = graph.get_object('/me/likes',fields='id,name,created_time')
for one_like in like_info['data']:
    def like_name():
        try:
            return ones_like['name']
        except:
            return 'No_Name'
        
    ins = likes.insert().values(
        user_id = user_info['id'],
        page_name = like_name(),
        page_id =  one_like['id'],
        like_date_time = one_like['created_time']
    )
    print(str(ins))

    print(ins.compile().params)

    result = conn.execute(ins)

    print('Last inserted key:')

    print(result.inserted_primary_key)