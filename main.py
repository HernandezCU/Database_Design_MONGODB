import pymongo, random, pprint
from faker import Faker

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client["mySocial"]

def add_user():
    USER = db["User_COLL"]
    u = {"name": Faker().name(), 
         "age": Faker().random_int(min=18, max=100), 
         "email": Faker().email(), 
         "password": Faker().password(), 
         "address": Faker().address()}
    user = USER.insert_one(u)
    return user.inserted_id

def add_post():
    POST = db["Post_COLL"]
    ids = [str(id) for id in db["User_COLL"].find().distinct('_id')]
    p = {
        "user_id": random.choice(ids),
        "title": Faker().sentence(nb_words=6, variable_nb_words=True), 
        "content": Faker().paragraph(nb_sentences=3, variable_nb_sentences=True), 
        "date": Faker().date()
        }
    post = POST.insert_one(p)
    return post.inserted_id

def add_user_activity():
    ids = [str(id) for id in db["User_COLL"].find().distinct('_id')]
    USER_ACTIVITY = db["User_Activity_COLL"]
    ua = {
         "user_id" : random.choice(ids),
         "status": random.choice(["online", "offline"]), 
         "last_seen": Faker().date_time(), 
         "last_location": Faker().address()
         }
    user_activity = USER_ACTIVITY.insert_one(ua)
    return user_activity.inserted_id  

def display_data(d):
    pprint.pprint(d)
    print("\n")

if __name__ == "__main__":
    while True:
        x = input("Append Commands: add_user (ad), add_post (ap), add_user_activity (aua), exit (e) or to view records (db): ")
        if x == "ad":
            print("User Added! \nID:" + str(add_user()))
        elif x == "ap":
            print("Post Added! \nID:" + str(add_post()))
        elif x == "aua":
            print("User Activity Added! \nID:" + str(add_user_activity()))
        elif x == "e":
            break
        elif x == "db":
            while True:
                z = input("View Commands: User (u), Post (p), User Activity (ua), exit (e): ")
                if z == "u":
                    for i in db["User_COLL"].find():
                        display_data(i)
                elif z == "p":
                    for i in db["Post_COLL"].find():
                        display_data(i)
                elif z == "ua":
                    for i in db["User_Activity_COLL"].find():
                        display_data(i)
                elif z == "e":
                    break
                else:
                    print("Invalid Command!")
        else:
            print("Invalid Command!")
    
