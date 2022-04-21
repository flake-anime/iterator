import os
from pymongo import MongoClient

class Database:

    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client.anime_database

    def insert_data(self, data):
        self.db.anime_collection.insert_one(data)
