# -*- coding: utf-8 -*-

"""
A set of unit tests for testing if the profiles module is working properly
@author: Darren
"""
import unittest

from views.helpers import connect
import views.profiles as profile

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(Test, cls).setUpClass()
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
    
    @classmethod
    def tearDownClass(cls):
        super(Test, cls).tearDownClass()
        cls.client.close()

if __name__ == "__main__":
    unittest.main()