from dotenv import dotenv_values
from data_reader import generateUserAndMovieDocs
from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint

# Load credentials
config = dotenv_values(".env")
username = config['USER']
key = config['PASSWORD']

# connect to MongoDB
client = MongoClient(f"mongodb+srv://{username}:{key}@cluster0.hynxe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db=client.taller

user_docs, movies_docs = generateUserAndMovieDocs()
movies_list = movies_docs.values()
users_list = user_docs.values()
movies_col = db['movies']
movies_col.insert_many(movies_list)
users_col = db['users']
users_col.insert_many(users_list)