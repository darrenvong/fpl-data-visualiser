# -*- coding: utf-8 -*-

"""
@author: Darren
"""
import attribute

attr = "cleanSheets"

def get_over_time_data(col, player_name, start, end):
    return attribute.get_over_time_data(col, player_name, start, end, attr)

def get_home_vs_away_data(col, player_name, start, end):
    return attribute.get_home_vs_away_data(col, player_name, start, end, attr)

def get_cumulative_total_data(col, player_name, start, end):
    return attribute.get_cumulative_total_data(col, player_name, start, end, attr)