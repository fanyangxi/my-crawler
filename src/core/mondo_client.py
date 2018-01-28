from pymongo import MongoClient


class MyMongoClient():
    def sample(self):
        client = MongoClient('mongodb://localhost:27017/')
        db = client['test-database']  # db = client.test_database
        collection = db['test-collection']