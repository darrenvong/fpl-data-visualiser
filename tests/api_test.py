# -*- coding: utf-8 -*-

"""
A set of unit tests for testing if the API is working properly
@author: Darren
"""
import unittest
import profile_graph_api
import helpers

class Test(unittest.TestCase):
    def setUp(self):
        self.player_name = "Vardy"
        self.start = 5 # Week 5
        self.end = 9 # Week 9
        self.client, self.col = helpers.connect()
    
    @unittest.skip("Don't run this so that MongoDB ports are not exhausted!")
    def test_over_time_data_points(self):
        data = profile_graph_api.get_over_time_data(self.col, self.player_name,
                                                    self.start, self.end, "points")
        expected = {"x": 5, "y": 6, "name": "AVL(H) 3-2"}
        self.assertEqual(data[0], expected)
    
    @unittest.skip("Don't run this so that MongoDB ports are not exhausted!")
    def test_home_away_data_points(self):
        data = profile_graph_api.get_home_vs_away_data(self.col, self.player_name,
                                                       self.start, self.end, "points")
        self.assertEqual(data, [{u'y': 18, 'name': 'Home'}, {u'y': 28, 'name': 'Away'}])
    
    @unittest.skip("Don't run this so that MongoDB ports are not exhausted!")
    def test_consistency_data_points(self):
        data = profile_graph_api.get_consistency_data(self.col, self.player_name,
                                                      self.start, self.end, "points")
        self.assertEqual(data, [[6, 7.5, 9.0, 12.5, 13]])
    
    @unittest.skip("Don't run this so that MongoDB ports are not exhausted!")
    def test_cumulative_data_points(self):
        data = profile_graph_api.get_cumulative_total_data(self.col, self.player_name,
                                                           self.start, self.end, "points")
        expected = [[5, 6], [6, 12], [7, 24], [8, 33], [9, 46]]
        self.assertEqual(data, expected)

    @unittest.skip("Don't run this so that MongoDB ports are not exhausted!")
    def test_events_bd_data_points(self):
        data = profile_graph_api.get_events_breakdown_data(self.col, self.player_name,
                                                           self.start, self.end, "points")
        expected = [{'goals': [[5, 4], [6, 4], [7, 8], [8, 4], [9, 8]]},
                    {'assists': [[5, 0], [6, 0], [7, 0], [8, 0], [9, 0]]},
                    {'others': [[5, 2], [6, 2], [7, 4], [8, 5], [9, 5]]}]
        self.assertEqual(data, expected)
    
#     @unittest.skip("Don't run this so that MongoDB ports are not exhausted!")
    def test_events_bd_data_points_def(self):
        data = profile_graph_api.get_events_breakdown_data(self.col, "Bellerin",
                                                           self.start, self.end, "points")
        expected = [{'goals': [[5,0], [6,0], [7,0], [8,0], [9,0]]},
                    {'assists': [[5,0], [6,0], [7,3], [8,0], [9,3]]},
                    {'cleanSheets': [[5,4], [6,0], [7,0], [8,4], [9,4]]},
                    {'others': [[5,5], [6,1], [7,1], [8,3], [9,3]]}]
        self.assertEqual(data, expected)        
    
#     @unittest.skip("Don't run this so that MongoDB ports are not exhausted!")
    def test_over_time_data_price(self):
        data = profile_graph_api.get_over_time_data(self.col, self.player_name,
                                                    self.start, self.end, "price")
        expected = [[5, 6.1], [6, 6.2], [7, 6.3], [8, 6.6], [9, 6.8]]
        self.assertEqual(data, expected)
    
#     @unittest.skip("Results out dated. Update them before reactivating tests")
    def test_get_changes_data_price(self):
        data = profile_graph_api.get_changes_data(self.col, self.player_name,
                                                  self.start, self.end, "price")
        expected = [[5, 0], [6, 0.1], [7, 0.1], [8, 0.3], [9, 0.2]]
        self.assertEqual(data, expected)
    
    @unittest.skip("Results out dated. Update them before reactivating tests")
    def test_over_time_data_goals(self):
        data = profile_graph_api.get_over_time_data(self.col, self.player_name,
                                                    self.start, self.end, "goals")
        expected = [[5, 1], [6, 1], [7, 2], [8, 1], [9, 2], [10, 1],
                    [11, 1], [12, 1], [13, 1], [14, 1]]
        self.assertEqual(data, expected)
    
    @unittest.skip("Results out dated. Update them before reactivating tests")
    def test_home_away_data_goals(self):
        data = profile_graph_api.get_home_vs_away_data(self.col, self.player_name,
                                                       self.start, self.end, "goals")
        expected = [{u'y': 6, 'name': 'Home'}, {u'y': 6, 'name': 'Away'}]
        self.assertEqual(data, expected)
    
    @unittest.skip("Results out dated. Update them before reactivating tests")
    def test_cumulative_data_goals(self):
        data = profile_graph_api.get_cumulative_total_data(self.col, self.player_name,
                                                       self.start, self.end, "goals")
        expected = [[5, 1], [6, 2], [7, 4], [8, 5], [9, 7], [10, 8],
                    [11, 9], [12, 10], [13, 11], [14, 12]]
        self.assertEqual(data, expected)
    
    @unittest.skip("Results out dated. Update them before reactivating tests")
    def test_over_time_data_assists(self):
        data = profile_graph_api.get_over_time_data(self.col, self.player_name,
                                                    self.start, self.end, "assists")
        expected = [[5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0],
                    [11, 0], [12, 0], [13, 0], [14, 0]]
        self.assertEqual(data, expected)
    
    @unittest.skip("Results out dated. Update them before reactivating tests")
    def test_home_away_data_assists(self):
        data = profile_graph_api.get_home_vs_away_data(self.col, self.player_name,
                                                       self.start, self.end, "assists")
        expected = [{u'y': 0, 'name': 'Home'}, {u'y': 0, 'name': 'Away'}]
        self.assertEqual(data, expected)
    
    @unittest.skip("Results out dated. Update them before reactivating tests")
    def test_cumulative_data_assists(self):
        data = profile_graph_api.get_cumulative_total_data(self.col, self.player_name,
                                                       self.start, self.end, "assists")
        expected = [[5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0],
                    [11, 0], [12, 0], [13, 0], [14, 0]]
        self.assertEqual(data, expected)
    
    @unittest.skip("Results out dated. Update them before reactivating tests")
    def test_over_time_data_cs(self):
        data = profile_graph_api.get_over_time_data(self.col, "Cech",
                                                    self.start, self.end, "cleanSheets")
        expected = [[5, 1], [6, 0], [7, 0], [8, 1], [9, 1], [10, 0],
                    [11, 1], [12, 0], [13, 0], [14, 0]]
        self.assertEqual(data, expected)
    
    @unittest.skip("Results out dated. Update them before reactivating tests")
    def test_home_away_data_cs(self):
        data = profile_graph_api.get_home_vs_away_data(self.col, "Cech",
                                                       self.start, self.end, "cleanSheets")
        expected = [{u'y': 2, 'name': 'Home'}, {u'y': 2, 'name': 'Away'}]
        self.assertEqual(data, expected)
    
    @unittest.skip("Results out dated. Update them before reactivating tests")
    def test_cumulative_data_cs(self):
        data = profile_graph_api.get_cumulative_total_data(self.col, "Cech",
                                                       self.start, self.end, "cleanSheets")
        expected = [[5, 1], [6, 1], [7, 1], [8, 2], [9, 3], [10, 3],
                    [11, 4], [12, 4], [13, 4], [14, 4]]
        self.assertEqual(data, expected)
    
    @unittest.skip("Results out dated. Update them before reactivating tests")
    def test_over_time_data_transfers(self):
        data = profile_graph_api.get_over_time_data(self.col, self.player_name,
                                                       self.start, self.end, "netTransfers")
        expected = [[5, 61918], [6, 98655], [7, 56460], [8, 504523], [9, 241805],
                    [10, 368617], [11, 150856], [12, 137586], [13, 17469], [14, 70351]]
        self.assertEqual(data, expected)
    
    @unittest.skip("Results out dated. Update them before reactivating tests")
    def test_over_time_data_mins_played(self):
        data = profile_graph_api.get_over_time_data(self.col, self.player_name,
                                                       self.start, self.end, "minutesPlayed")
        expected = [[5, 90], [6, 90], [7, 90], [8, 90], [9, 90],
                    [10, 90], [11, 90], [12, 90], [13, 76], [14, 90]]
        self.assertEqual(data, expected)
    
    def tearDown(self):
        self.client.close()


if __name__ == "__main__":
    unittest.main()