# -*- coding: utf-8 -*-

"""
A set of unit tests for testing if the home module generates the tables correctly
@author: Darren Vong
"""
import unittest

import views.home as home
from views.helpers import connect

class TestHome(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestHome, cls).setUpClass()
        cls.client, cls.col = connect()

    def test_table_hot_players(self):
        hot_players_list = home.get_hot_players(self.col)
        table = home.generate_tables(hot_players_list, "hot_players")
        self.assertIn(u"<td>£", table)
        self.assertRegexpMatches(table, "<td>(\d)+\.(\d)+")
    
    def test_table_pound_stretchers(self):
        pound_stretchers = home.pound_stretchers(self.col)
        table = home.generate_tables(pound_stretchers)
        self.assertIn(u"<td>£", table)
        self.assertRegexpMatches(table, "<td>[a-zA-Z]+</td>")
    
    def test_table_most_popular(self):
        most_popular = home.most_popular(self.col)
        table = home.generate_tables(most_popular, "popular_players")
        self.assertIn(u"<td>£", table)
        self.assertRegexpMatches(table, "<td>[+-](\d)+")


if __name__ == "__main__":
    unittest.main()