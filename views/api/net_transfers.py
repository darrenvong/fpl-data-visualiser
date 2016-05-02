# -*- coding: utf-8 -*-

"""
This module models the "Net transfers" attribute in a player profile or head-to-head
comparator's page table and provides functions for getting data of all the relevant
metrics available to "Net transfers".
@author: Darren Vong
"""
import attribute

attr = "netTransfers"

def get_over_time_data(col, player_name, start, end):
    return attribute.get_over_time_data(col, player_name, start, end, attr)
