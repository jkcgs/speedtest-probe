import pymongo
from pymongo import MongoClient

from . import settings
from .logger import logger

client = MongoClient(settings.get('database-uri'))
db = client.get_database()
ms = db.get_collection('measurements')
ms.create_index([('timestamp', pymongo.DESCENDING)])

logger.info('Connected to database, %s measurement entries found', ms.count())


def get_results(limit=10):
    n_servers = len(settings.get('servers'))
    return ms.find(limit=limit*n_servers)


def insert_result(result):
    ms.insert_one(result)
