from pymongo import MongoClient

def get_mongo_client():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["refeicoes"]  
    return db
