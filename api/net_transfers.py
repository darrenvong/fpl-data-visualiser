# -*- coding: utf-8 -*-

"""
@author: Darren
"""
import attribute

attr = "netTransfers"

def get_over_time_data(col, player_name, start, end):
    return attribute.get_over_time_data(col, player_name, start, end, attr)