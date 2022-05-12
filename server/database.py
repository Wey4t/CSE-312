import pymongo
import json
USER = "user_identity"
MESSAGE = "message_history"
PROFILE = "user_profile"
USER_STATUS = "user_status"
PFP_ID = "pfp_id"
client = pymongo.MongoClient(port=27017)
db=client["web_project"]
collection_map = {}
def add_table(table_name, key):
    coll = db[table_name]
    key = tuple(sorted(key.keys()))
    collection_map[key]=coll
add_table(USER_STATUS, {'username':'','status':''})
add_table(USER, {'username':'','hash':'','token':'','salt':''})
add_table(MESSAGE, {'sender':'','receiver':'','message':'','message_status':''})
add_table(PROFILE, {'username':'','post':'','profile':'','profile_image':''})
add_table(PFP_ID, {"last_pfp_id": -1})
def nothing(x):
    pass

def insert(insert_dict):
    insert_dict_key = tuple(sorted(insert_dict.keys()))
    collection_map[insert_dict_key].insert_one(insert_dict)

def find(collection_name,query = {},func = nothing):
    collection = db[collection_name]
    all = collection.find_one(query)
    return all
def find_all(collection_name,query = {},func = nothing):
    collection = db[collection_name]
    all = collection.find(query)
    return list(all)

def delete(collection_name,query,many = False):
    collection = db[collection_name]
    if many:
        collection.delete_many(query)
    else:    
        collection.delete_one(query)

def update(collection_name,query,value,many = False):
    collection = db[collection_name]
    newvalues = {"$set": value}
    if many:
        collection.update_many(query, newvalues)
    else:    
        collection.update_one(query, newvalues)
    
# test
