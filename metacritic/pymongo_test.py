import pymongo
import pprint
import datetime
client = pymongo.MongoClient(
    "mongodb+srv://fxy7999148:operation@mflix-3brpa.mongodb.net/test")
db = client.metacritic

print(db)

post = [{
    "author": "Hsin",
    "Text": "what is new?",
    "date": datetime.datetime.utcnow(),
    "label": "old"
}, {
    "author": "Feyzi",
    "Text": "Pimp new?",
    "date": datetime.datetime.utcnow(),
}, {
    "author": "Hsin",
    "Text": "what is new?",
    "date": datetime.datetime.utcnow(),
    "label": "new",
    "www": 'www'
}]

posts = db.posts
for i in range(len(post)):
    posts.update(
        {
            "$and": [{
                "author": post[i]["author"]
            }, {
                "label": "new"
            }]
        },
        post[i],
        upsert=True)
