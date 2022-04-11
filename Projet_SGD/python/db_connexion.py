from pymongo import MongoClient
from bson.objectid import ObjectId
url="mongodb://br683616:br683616@mongo/?authSource=br683616&authMechanism=SCRAM-SHA-1"
c = MongoClient(url)
db = c.br683616
