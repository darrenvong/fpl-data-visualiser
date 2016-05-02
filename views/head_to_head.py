# -*- coding: utf-8 -*-

"""
@author: Darren Vong
"""
from collections import OrderedDict

import profiles

# Attributes here are properly separated words rather than camel cased attributes
# as in the module api.attribute
ATTR_TO_PROFILE_KEY = OrderedDict([
    ("Points", "total_points"),
    ("Selected By", "selected_by_percent"),
    ("Price", "now_cost"),
    ("Goals", "goals_scored"),
    ("Assists", "assists"),
    ("Clean sheets", "clean_sheets"),
    ("Yellow cards", "yellow_cards")
])

def get_players_profiles(player1, player2, col):
    """Finds the two players' profiles searched for.
    @param player1: name of the first player's profile to search for
    @param player2: name of the second player's profile to search for
    @param col: the MongoDB database collection to search the profiles from
    @return a tuple containing both players' profile data held in a dictionary.
    """
    
    player1_profile = profiles.get_profile_contents(player1, col)
    player2_profile = profiles.get_profile_contents(player2, col)
    return player1_profile, player2_profile

def generate_table(p1_profile, p2_profile):
    """Generates a head-to-head comparison table using the player profiles data.
    @param p1_profile: the first player's profile
    @param p2_profile: the second player's profile
    @return the HTML for generating most of the table body in the head-to-head page template
    """
    
    table = u""
    for attr in ATTR_TO_PROFILE_KEY.iterkeys():
        table += generate_row(p1_profile, p2_profile, attr)
    
    return table 

def generate_row(p1_profile, p2_profile, attr):
    """Generates a row of the head-to-head comparison table for the attribute specified.
    @param p1_profile: the first player's profile
    @param p2_profile: the second player's profile
    @param attr: the attribute to use to generate this row of the table
    @return the row in HTML for the attribute
    """
    
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
    """Auxiliary function for generate_row above - this function contains the logic
    for deciding which value cell is highlighted (by adding the *-success CSS classes)
    depending on the value and the attribute specified.
    @param p1_val: the attribute value of the first player
    @param p2_val: the attribute value of the second player
    @param attr: the attribute to use for the table row
    @keyword prefix: the characters to insert before the value of the attribute
    @keyword suffix: the characters to insert after the value of the attribute
    @return the row in HTML for the attribute with the superior value highlighted
    """
    
    row = u""
    if p1_val > p2_val:
        row = u"<tr class='"+ATTR_TO_PROFILE_KEY[attr]+u"'>\n"
        if attr == "Price" or attr == "Yellow cards":
            row += u"<td class='values p1'>"+prefix+unicode(p1_val)+suffix+u"</td>\n"
        else:
            row += u"<td class='values p1 text-success bg-success'>"+prefix+unicode(p1_val)+suffix+u"</td>\n"
        row += u"<td>"+attr+u"</td>\n"
        if attr == "Price" or attr == "Yellow cards":
            row += u"<td class='values p2 text-success bg-success'>"+prefix+unicode(p2_val)+suffix+u"</td>\n"
        else:
            row += u"<td class='values p2'>"+prefix+unicode(p2_val)+suffix+u"</td>\n"
        row += u"</tr>\n"
    elif p1_val == p2_val:
        row = u"<tr class='"+ATTR_TO_PROFILE_KEY[attr]+u"'>\n"
        row += u"<td class='values p1'>"+prefix+unicode(p1_val)+suffix+u"</td>\n"
        row += u"<td>"+attr+u"</td>\n"
        row += u"<td class='values p2'>"+prefix+unicode(p2_val)+suffix+u"</td>\n"
        row += u"</tr>\n"
    else: # p2 > p1
        row = u"<tr class='"+ATTR_TO_PROFILE_KEY[attr]+u"'>\n"
        if attr == "Price" or attr == "Yellow cards":
            row += u"<td class='values p1 text-success bg-success'>"+prefix+unicode(p1_val)+suffix+u"</td>\n"
        else:
            row += u"<td class='values p1'>"+prefix+unicode(p1_val)+suffix+u"</td>\n"
        row += u"<td>"+attr+u"</td>\n"
        if attr == "Price" or attr == "Yellow cards":
            row += u"<td class='values p2'>"+prefix+unicode(p2_val)+suffix+u"</td>\n"
        else:
            row += u"<td class='values p2 text-success bg-success'>"+prefix+unicode(p2_val)+suffix+u"</td>\n"
        row += u"</tr>\n"
    return row
