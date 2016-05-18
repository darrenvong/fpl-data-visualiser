# -*- coding: utf-8 -*-

"""
The top-level module is run in order to collect data and
ensure they remain up to date for the project's MongoDB database.
@author: Darren Vong
"""
import sys

from scraper import scrape_players
from db_updater import insert_players, enforce_injective_name_mapping, update_heroku_db
from views.helpers import connect

client, col = connect()
try:
    players_list = scrape_players()
except:
    sys.exit(1)
else:
    insert_players(col, players_list)
    enforce_injective_name_mapping(col)
finally:
    client.close()

# update_heroku_db(client)