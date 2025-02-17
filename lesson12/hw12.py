from pymongo import MongoClient

MONGO_URI = "mongodb+srv://oliversunwc:imgrackinit226@offsec.qw5ug.mongodb.net/"
client = MongoClient(MONGO_URI)

# Select the database and collection
db = client['test']
users_collection = db['users']

# Data to insert
users_data = [
    { "idx": 0, "username": "admin", "password": "pass" },
    { "idx": 1, "username": "noob", "password": "fail" }
]

# Insert the data
result = users_collection.insert_many(users_data)