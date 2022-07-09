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

# Get matching from DB
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
        # Finding matching score
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

        # Only use top 10 matching score
        {
            "$match": {
                "$expr": {"$gt": ["$matching_score", 0]}
            }
        },
        {
            "$sort": {"matching_score": -1}
        },
        {
            "$limit": 10
        },

        # Changing array to skills so it can be converted into table
        {
            "$addFields": {
                "skills": { "$reduce": {
                    "input": "$skills",
                    "initialValue": "",
                    "in": { "$concat": [
                        "$$value",
                        { "$cond": {
                                "if": { "$eq": [ "$$value", "" ] },
                                "then": "",
                                "else": ", "
                        }},
                        "$$this"                    
                    ]}
                }},
                "programming": { "$reduce": {
                    "input": "$programming",
                    "initialValue": "",
                    "in": { "$concat": [
                        "$$value",
                        { "$cond": {
                                "if": { "$eq": [ "$$value", "" ] },
                                "then": "",
                                "else": ", "
                        }},
                        "$$this"                    
                    ]}
                }},
                "framework": { "$reduce": {
                    "input": "$framework",
                    "initialValue": "",
                    "in": { "$concat": [
                        "$$value",
                        { "$cond": {
                                "if": { "$eq": [ "$$value", "" ] },
                                "then": "",
                                "else": ", "
                        }},
                        "$$this"                    
                    ]}
                }},                
            }
        }
    ]

    try: 
        return collection.aggregate(query)
    except:
        return 0