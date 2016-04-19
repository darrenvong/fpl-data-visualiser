# -*- coding: utf-8 -*-

"""
A set of unit tests for testing if the API is working properly
@author: Darren
"""
import unittest

from views import profile_graph_api, helpers

class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestAPI, cls).setUpClass()
        cls.player_name = "Vardy"
        cls.start = 5 # Week 5
        cls.end = 9 # Week 9
        cls.client, cls.col = helpers.connect()
    
    def test_over_time_data_points(self):
        data = profile_graph_api.get_over_time_data(self.col, self.player_name,
                                                    self.start, self.end, "points")
        expected = {"x": 5, "y": 6, "name": "AVL(H) 3-2"}
        self.assertEqual(data[0], expected)
    
    def test_home_away_data_points(self):
        data = profile_graph_api.get_home_vs_away_data(self.col, self.player_name,
                                                       self.start, self.end, "points")
        self.assertEqual(data, [{u'y': 18, 'name': 'Home'}, {u'y': 28, 'name': 'Away'}])
    
    def test_consistency_data_points(self):
        data = profile_graph_api.get_consistency_data(self.col, self.player_name,
                                                      self.start, self.end, "points")
        self.assertEqual(data, [[6, 7.5, 9.0, 12.5, 13]])
    
    def test_cumulative_data_points(self):
        data = profile_graph_api.get_cumulative_total_data(self.col, self.player_name,
                                                           self.start, self.end, "points")
        expected = [[5, 6], [6, 12], [7, 24], [8, 33], [9, 46]]
        self.assertEqual(data, expected)

    def test_events_bd_data_points(self):
        data = profile_graph_api.get_events_breakdown_data(self.col, self.player_name,
                                                           self.start, self.end, "points")
        expected = [{'goals': [[5, 4], [6, 4], [7, 8], [8, 4], [9, 8]]},
                    {'assists': [[5, 0], [6, 0], [7, 0], [8, 0], [9, 0]]},
                    {'others': [[5, 2], [6, 2], [7, 4], [8, 5], [9, 5]]}]
        self.assertEqual(data, expected)
    
    def test_events_bd_data_points_def(self):
        data = profile_graph_api.get_events_breakdown_data(self.col, "Bellerin",
                                                           self.start, self.end, "points")
        expected = [{'goals': [[5,0], [6,0], [7,0], [8,0], [9,0]]},
                    {'assists': [[5,0], [6,0], [7,3], [8,0], [9,3]]},
                    {'cleanSheets': [[5,4], [6,0], [7,0], [8,4], [9,4]]},
                    {'others': [[5,5], [6,1], [7,1], [8,3], [9,3]]}]
        self.assertEqual(data, expected)        
    
    def test_over_time_data_price(self):
        data = profile_graph_api.get_over_time_data(self.col, self.player_name,
                                                    self.start, self.end, "price")
        expected = [[5, 6.1], [6, 6.2], [7, 6.3], [8, 6.6], [9, 6.8]]
        self.assertEqual(data, expected)
    
    def test_get_changes_data_price(self):
        data = profile_graph_api.get_changes_data(self.col, self.player_name,
                                                  self.start, self.end, "price")
        expected = [[5, 0], [6, 0.1], [7, 0.1], [8, 0.3], [9, 0.2]]
        self.assertEqual(data, expected)
    
    def test_over_time_data_goals(self):
        data = profile_graph_api.get_over_time_data(self.col, self.player_name,
                                                    self.start, self.end, "goals")
        expected = [{'name': u'AVL(H) 3-2', 'x': 5, 'y': 1}, {'name': u'STK(A) 2-2', 'x': 6, 'y': 1},
                    {'name': u'ARS(H) 2-5', 'x': 7, 'y': 2}, {'name': u'NOR(A) 2-1', 'x': 8, 'y': 1},
                    {'name': u'SOU(A) 2-2', 'x': 9, 'y': 2}]
        self.assertEqual(data, expected)
    
    def test_home_away_data_goals(self):
        data = profile_graph_api.get_home_vs_away_data(self.col, self.player_name,
                                                       self.start, self.end, "goals")
        expected = [{u'y': 3, 'name': 'Home'}, {u'y': 4, 'name': 'Away'}]
        self.assertEqual(data, expected)
    
    def test_cumulative_data_goals(self):
        data = profile_graph_api.get_cumulative_total_data(self.col, self.player_name,
                                                       self.start, self.end, "goals")
        expected = [[5, 1], [6, 2], [7, 4], [8, 5], [9, 7]]
        self.assertEqual(data, expected)
    
    def test_over_time_data_assists(self):
        data = profile_graph_api.get_over_time_data(self.col, self.player_name,
                                                    self.start, self.end, "assists")
        expected = [{'name': u'AVL(H) 3-2', 'x': 5, 'y': 0},{'name': u'STK(A) 2-2', 'x': 6, 'y': 0},
                    {'name': u'ARS(H) 2-5', 'x': 7, 'y': 0},{'name': u'NOR(A) 2-1', 'x': 8, 'y': 0},
                    {'name': u'SOU(A) 2-2', 'x': 9, 'y': 0}]
        self.assertEqual(data, expected)
    
    def test_home_away_data_assists(self):
        data = profile_graph_api.get_home_vs_away_data(self.col, self.player_name,
                                                       self.start, self.end, "assists")
        expected = [{u'y': 0, 'name': 'Home'}, {u'y': 0, 'name': 'Away'}]
        self.assertEqual(data, expected)
    
    def test_cumulative_data_assists(self):
        data = profile_graph_api.get_cumulative_total_data(self.col, self.player_name,
                                                       self.start, self.end, "assists")
        expected = [[5, 0], [6, 0], [7, 0], [8, 0], [9, 0]]
        self.assertEqual(data, expected)
    
    def test_over_time_data_cs(self):
        data = profile_graph_api.get_over_time_data(self.col, "Cech",
                                                    self.start, self.end, "cleanSheets")
        expected = [{'name': u'STK(H) 2-0', 'x': 5, 'y': 1}, {'name': u'CHE(A) 0-2', 'x': 6, 'y': 0},
                    {'name': u'LEI(A) 5-2', 'x': 7, 'y': 0}, {'name': u'MUN(H) 3-0', 'x': 8, 'y': 1},
                    {'name': u'WAT(A) 3-0', 'x': 9, 'y': 1}]
        self.assertEqual(data, expected)
    
    def test_home_away_data_cs(self):
        data = profile_graph_api.get_home_vs_away_data(self.col, "Cech",
                                                       self.start, self.end, "cleanSheets")
        expected = [{u'y': 2, 'name': 'Home'}, {u'y': 1, 'name': 'Away'}]
        self.assertEqual(data, expected)
    
    def test_cumulative_data_cs(self):
        data = profile_graph_api.get_cumulative_total_data(self.col, "Cech",
                                                       self.start, self.end, "cleanSheets")
        expected = [[5, 1], [6, 1], [7, 1], [8, 2], [9, 3]]
        self.assertEqual(data, expected)
    
    def test_over_time_data_transfers(self):
        data = profile_graph_api.get_over_time_data(self.col, self.player_name,
                                                       self.start, self.end, "netTransfers")
        expected = [{'name': u'AVL(H) 3-2', 'x': 5, 'y': 61918}, {'name': u'STK(A) 2-2', 'x': 6, 'y': 98655},
                    {'name': u'ARS(H) 2-5', 'x': 7, 'y': 56460}, {'name': u'NOR(A) 2-1', 'x': 8, 'y': 504523},
                    {'name': u'SOU(A) 2-2', 'x': 9, 'y': 241805}]
        self.assertEqual(data, expected)
    
    def test_over_time_data_mins_played(self):
        data = profile_graph_api.get_over_time_data(self.col, self.player_name,
                                                       self.start, self.end, "minutesPlayed")
        expected = [{'name': u'AVL(H) 3-2', 'x': 5, 'y': 90}, {'name': u'STK(A) 2-2', 'x': 6, 'y': 90},
                    {'name': u'ARS(H) 2-5', 'x': 7, 'y': 90}, {'name': u'NOR(A) 2-1', 'x': 8, 'y': 90},
                    {'name': u'SOU(A) 2-2', 'x': 9, 'y': 90}]
        self.assertEqual(data, expected)
    
    @classmethod
    def tearDownClass(cls):
        super(TestAPI, cls).tearDownClass()
        cls.client.close()


if __name__ == "__main__":
    unittest.main()