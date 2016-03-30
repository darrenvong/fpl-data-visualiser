# -*- coding: utf-8 -*-

"""
@author: Darren Vong
"""
import profiles

ATTR_TO_PROFILE_KEY = {
    "Points": "total_points",
    "Selected By": "selected_by_percent",
    "Price": "now_cost",
    "Goals": "goals_scored",
    "Assists": "assists",
    "Clean sheets": "clean_sheets",
    "Yellow cards": "yellow_cards"
}

def get_players_profiles(player1, player2, col):
    player1_profile = profiles.get_profile_contents(player1, col)
    player2_profile = profiles.get_profile_contents(player2, col)
    return player1_profile, player2_profile

def generate_table(p1_profile, p2_profile):
    table = u""
    for attr in ATTR_TO_PROFILE_KEY.iterkeys():
        table += generate_row(p1_profile, p2_profile, attr)
    
    return table 

def generate_row(p1_profile, p2_profile, attr):
    integer_val_attr = ["Points", "Goals", "Assists", "Yellow cards", "Clean sheets"]
    if attr in integer_val_attr:
        p1_val = int(p1_profile[ATTR_TO_PROFILE_KEY[attr]])
        p2_val = int(p2_profile[ATTR_TO_PROFILE_KEY[attr]])
        row = row_template(p1_val, p2_val, attr)
    elif attr == "Price":
        p1_val = p1_profile[ATTR_TO_PROFILE_KEY[attr]]/10.0 
        p2_val = p2_profile[ATTR_TO_PROFILE_KEY[attr]]/10.0
        row = row_template(p1_val, p2_val, attr, prefix=u"£", suffix=u"M")
    else:
        p1_val = float(p1_profile[ATTR_TO_PROFILE_KEY[attr]])
        p2_val = float(p2_profile[ATTR_TO_PROFILE_KEY[attr]])
        row = row_template(p1_val, p2_val, attr, suffix=u"%")
    return row

def row_template(p1_val, p2_val, attr, prefix=u"", suffix=u""):
    row = u""
    if p1_val > p2_val:
        row = u"<tr>\n"
        row += u"<td class='values text-success bg-success'>"+prefix+unicode(p1_val)+suffix+u"</td>\n"
        row += u"<td>"+attr+u"</td>\n"
        row += u"<td class='values'>"+prefix+unicode(p2_val)+suffix+u"</td>\n"
        row += u"</tr>\n"
    elif p1_val == p2_val:
        row = u"<tr>\n"
        row += u"<td class='values'>"+prefix+unicode(p1_val)+suffix+u"</td>\n"
        row += u"<td>"+attr+u"</td>\n"
        row += u"<td class='values'>"+prefix+unicode(p2_val)+suffix+u"</td>\n"
        row += u"</tr>\n"
    else:
        row = u"<tr>\n"
        row += u"<td class='values'>"+prefix+unicode(p1_val)+suffix+u"</td>\n"
        row += u"<td>"+attr+u"</td>\n"
        row += u"<td class='values text-success bg-success'>"+prefix+unicode(p2_val)+suffix+u"</td>\n"
        row += u"</tr>\n"
    return row