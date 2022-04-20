import pymongo
client = pymongo.MongoClient(port=27017)
db=client["web_project"]
collection_map = {}
def add_table(table_name, key):
    coll = db[table_name]
    key = tuple(sorted(key.keys()))
    collection_map[key]=coll
add_table("user_identity", {'username':'','email':'','shadow':''})
add_table("comment_space", {'username':'','comment':'','image':''})
def nothing(x):
    pass

def insert(insert_dict):
    insert_dict_key = tuple(sorted(insert_dict.keys()))
    collection_map[insert_dict_key].insert_one(insert_dict)

def find(collection_name,query = {},func = nothing):
    collection = db[collection_name]
    all = collection.find(query,{"_id": 0})
    result = []
    for x in all:
        func(x)
        result.append(x)
    return result

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
if __name__ == "__main__":
    test_case_1 = {'username':'Tom','email':'Tom@gmail.com','shadow':'ASdzfgz='}
    test_case_2 = {'username':'Jay','comment':'this is dog','image':'dog.jpg'}
    test_case_3 = {'username':'Zoe','comment':'this is cat','image':'cat.jpg'}
    #insert(test_case_1)
    #print(find('user_identity',{'username':'Tom'}))
    insert(test_case_2)
    print('before delete',find('comment_space',{'image':'dog.jpg'}))
    delete('comment_space',{'image':'dog.jpg'})
    print('after delete',find('comment_space',{'image':'dog.jpg'}))
    for x in range(1,10):
        test_case_3 = {'username':'Zoe','comment':'this is cat','image':'cat.jpg'} # insert will change test_case_3
        insert(test_case_3)
    print('before delete',find('comment_space',{'image':'cat.jpg'}))
    delete('comment_space',{'image':'cat.jpg'},True)
    print('after delete',find('comment_space',{'image':'cat.jpg'}))
    for x in range(1,10):
        test_case_3 = {'username':'Zoe','comment':'this is cat','image':'cat.jpg'} # insert will change test_case_3
        insert(test_case_3)
    print('before update one',find('comment_space',{'image':'cat.jpg'}))
    update('comment_space',{'image':'cat.jpg'},{'image':'dog.jpg'})
    print('after update one',find('comment_space'))
    update('comment_space',{'image':'cat.jpg'},{'image':'dog.jpg'},True)
    print('after update many',find('comment_space'))