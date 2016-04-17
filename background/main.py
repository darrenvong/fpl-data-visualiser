# -*- coding: utf-8 -*-

"""
The top-level module is run in order to collect data and
ensure they remain up to date for the project's MongoDB database.
@author: Darren Vong
"""

from scraper import scrape_players
from db_updater import insert_players, enforce_injective_name_mapping, update_heroku_db
from views.helpers import connect

client, col = connect()
players_list = scrape_players()
insert_players(col, players_list)
enforce_injective_name_mapping(col)

# update_heroku_db(client)