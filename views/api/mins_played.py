# -*- coding: utf-8 -*-

"""
This module models the "Minutes played" attribute in a player profile or head-to-head
comparator's page table and provides functions for getting data of all the relevant
metrics available to "Minutes played".
@author: Darren Vong
"""
import attribute

attr = "minutesPlayed"

def get_over_time_data(col, player_name, start, end):
    return attribute.get_over_time_data(col, player_name, start, end, attr)
