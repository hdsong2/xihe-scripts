# -*- coding: utf-8 -*-

from typing import Dict, Union
import urllib

from pymongo import MongoClient
from pymongo.database import Database

_client = None
_database = None

def initialize(config: Dict[str, Union[str, int]]):
    (rwuser, password, ip, port, database, ca_file) = \
    config['rwuser'], config['password'], config['ip'], config['port'], config['database'], config["cafile"]

    global _client, _database
    user = urllib.parse.quote_plus(rwuser)
    pwd = urllib.parse.quote_plus(password)

    uri = 'mongodb://{user}:{password}@{ip}:{port}/?authSource={db}'.format(
        user=user, password=pwd, ip=ip, port=port, db=database)
    _client = MongoClient(uri, connectTimeoutMS=5000, tls=True, tlsAllowInvalidHostnames=True, tlsCAFile=ca_file)
    _database = database

def db(name: str = None) -> Database:
    if _client == None or _database == None:
        raise Exception('please call mongo.initialize first')

    return _client[name if name else _database]

def close():
    if _client != None:
        _client.close()
