from pymongo import MongoClient
from bson.objectid import ObjectId
url="mongodb://ag425107:ag425107@mongo/?authSource=ag425107&authMechanism=SCRAM-SHA-1"
c = MongoClient(url)
db = c.ag425107
