"""
@author: Darren
"""

from pymongo import MongoClient

def connect():
    client = MongoClient()
    players = client.players.current_gw
    return client, players

if __name__ == "__main__":
    pass