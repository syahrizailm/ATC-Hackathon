from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Check local or prod
is_prod = os.environ.get('IS_HEROKU', None)

# Provide the mongodb atlas url to connect python to mongodb using pymongo
if is_prod:
    CONNECTION_STRING = os.environ.get('MONGO_CONNECTION')
else:
    load_dotenv()
    CONNECTION_STRING = os.environ["MONGO_CONNECTION"]

# Create a connection using MongoClient
client = MongoClient(CONNECTION_STRING)
db = client['portfolio_list']
collection = db["portfolio_collection"]

# Insert to DB
def insert(data):
    try:
        collection.insert_one(data)
        return 1
    except:
        return 0

def get_matching(condition):
    """
    Return query string for mongodb
    condition format:
    [
        {param: <>, value: <>],
        {param: <>, value: <>],
        ...
    ]
    """
    consolidate_condition = []
    for cond in condition:
        consolidate_condition.append(
            {"$toInt": {"$in": [cond["value"], f"${cond['param']}"]}}
        )

    query = [
        {
            "$addFields": {
                "matching_score": {
                    "$divide": [ 
                        {"$add": consolidate_condition},
                        len(condition)
                    ]
                }
            }
        },
        {
            "$match": {
                "$expr": {"$gt": ["$matching_score", 0]}
            }
        },
        {
            "$sort": {"matching_score": 1}
        }
    ]

    try: 
        return collection.aggregate(query)
    except:
        return 0