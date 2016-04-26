# -*- coding: utf-8 -*-

"""
A set of unit tests for testing if the profiles module is working properly
@author: Darren Vong
"""
import unittest

from views.helpers import connect
import views.profiles as profile

class TestProfiles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestProfiles, cls).setUpClass()
        cls.start, cls.end = 27, 32
        cls.name = "Mahrez"
        cls.client, cls.col = connect()
    
    def test_custom_capitalise(self):
        name_to_capitalise = profile.custom_capitalise("kane")
        self.assertEqual(name_to_capitalise, "Kane")
    
    def test_custom_capitalise2(self):
        name_to_cap = profile.custom_capitalise("mAHrEz")
        self.assertEqual(name_to_cap, "Mahrez")
    
    def test_custom_capitalise3(self):
        name_to_cap = profile.custom_capitalise("sergio aguero")
        self.assertEqual(name_to_cap, "Sergio Aguero")
    
    def test_custom_capitalise4(self):
        name_to_cap = profile.custom_capitalise("sErGio aguero")
        self.assertEqual(name_to_cap, "Sergio Aguero")
    
    def test_custom_capitalise5(self):
        name_to_cap = profile.custom_capitalise("sERgio AguEro")
        self.assertEqual(name_to_cap, "Sergio Aguero")
        
    def test_custom_capitalise_positive(self):
        # An already capitalised name should be intact
        name_to_cap = profile.custom_capitalise(self.name)
        self.assertEqual(name_to_cap, "Mahrez")
    
    def test_get_player_names(self):
        player_names = profile.get_player_names(self.col)
        self.assertIsInstance(player_names, list)
        self.assertIn("Vardy", player_names)
        self.assertIn("Kane", player_names)
        self.assertIn("Aguero", player_names)
    
    def test_get_profile_contents(self):
        profile_contents = profile.get_profile_contents(self.name, self.col)
        self.assertIn("web_name", profile_contents)
        self.assertIn("normalised_name", profile_contents)
        self.assertEqual(profile_contents["web_name"], "Mahrez")
    
    def test_get_profile_contents2(self):
        """Testing with player that has a two part names (either double-barrelled name
        or the result after enforce_injective_name_mapping being run on players with
        the same surname."""
        
        profile_contents = profile.get_profile_contents("Odjidja-ofoe", self.col)
        self.assertIn("web_name", profile_contents)
        self.assertIn("normalised_name", profile_contents)
        self.assertEqual(profile_contents["web_name"], "Odjidja-Ofoe")
    
    def test_get_profile_contents3(self):
        profile_contents = profile.get_profile_contents("Ashley williams", self.col)
        self.assertEqual(profile_contents["web_name"], "Williams")
    
    def test_get_graph_data_over_time(self):
        data = profile.get_graph_data("over_time", self.start, self.end, self.col, self.name, "points")
        expected = {"over_time": [{"y": 3, "x": 27, "name": "NOR(H) 1-0"},
                                  {"y": 6, "x": 28, "name": "WBA(H) 2-2"},
                                  {"y": 11, "x": 29, "name": "WAT(A) 1-0"},
                                  {"y": 3, "x": 30, "name": "NEW(H) 1-0"},
                                  {"y": 9, "x": 31, "name": "CRY(A) 1-0"},
                                  {"y": 3, "x": 32, "name": "SOU(H) 1-0"}]}
        self.assertEqual(data, expected)
    
    def test_get_graph_data_home_vs_away(self):
        data = profile.get_graph_data("home_vs_away", self.start, self.end, self.col,
                                      self.name, "points")
        expected = {"home_vs_away": [{"y": 15, "name": "Home"}, {"y": 20, "name": "Away"}]}
        self.assertEqual(data, expected)
    
    def test_get_graph_data_consistency(self):
        data = profile.get_graph_data("consistency", self.start, self.end, self.col, self.name, "points")
        expected = {"consistency": [[3, 3.0, 4.5, 7.5, 11]]}
        self.assertEqual(data, expected)
    
    def test_get_graph_data_cum_total(self):
        data = profile.get_graph_data("cum_total", self.start, self.end, self.col, self.name, "goals")
        expected = {"cum_total": [[27, 0], [28, 0], [29, 1], [30, 1], [31, 2], [32, 2]]}
        self.assertEqual(data, expected)
    
    def test_get_graph_data_events(self):
        data = profile.get_graph_data("events_breakdown", self.start, self.end, self.col,
                                      self.name, "points")
        expected = {"events_breakdown": [{"goals": [[27, 0], [28, 0], [29, 5], [30, 0], [31, 5], [32, 0]]},
                                         {"assists": [[27, 0], [28, 3], [29, 0], [30, 0], [31, 0], [32, 0]]},
                                         {"others": [[27, 3], [28, 3], [29, 6], [30, 3], [31, 4], [32, 3]]}]}
        self.assertEqual(data, expected)
    
    def test_get_graph_data_changes(self):
        data = profile.get_graph_data("changes", self.start, self.end, self.col, self.name, "price")
        expected = {"changes": [[27, 0.0], [28, 0.0], [29, 0.0],
                                [30, 0.10000000000000001], [31, 0.0], [32, 0.0]]}
        self.assertEqual(data, expected)
    
    @classmethod
    def tearDownClass(cls):
        super(TestProfiles, cls).tearDownClass()
        cls.client.close()

if __name__ == "__main__":
    unittest.main()