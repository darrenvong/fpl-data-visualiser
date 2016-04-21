# -*- coding: utf-8 -*-

"""
A set of unit tests for testing if the head_to_head module is working properly
@author: Darren
"""
import unittest

from views.helpers import connect
import views.head_to_head as hth

class TestHeadToHead(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestHeadToHead, cls).setUpClass()
        cls.name, cls.name2 = "Mahrez", "Kane"
        cls.start, cls.end = 27, 33
        cls.client, cls.col = connect()
        cls.prof1, cls.prof2 = hth.get_players_profiles(cls.name, cls.name2, cls.col)
    
    def test_get_profiles(self):
        player1, player2 = hth.get_players_profiles(self.name, self.name2, self.col)
        self.assertEqual(player1["web_name"], "Mahrez")
        self.assertEqual(player2["web_name"], "Kane")
    
    def test_get_profiles_negative(self):
        self.assertRaises(StopIteration, hth.get_players_profiles, self.name, "ashley Williams", self.col)
    
    def test_get_profiles2(self):
        player1, player2 = hth.get_players_profiles("Ashley williams", "Bellerin", self.col)
        self.assertIn("web_name", player1)
        self.assertEqual(player1["web_name"], "Williams")
        self.assertEqual(player2["web_name"], u"Bellerín")
    
    def test_row_template_p1_lt_p2(self):
        """player 1 has a smaller value than player 2
        i.e. Mahrez has scored fewer goals than Kane (as of gameweek 34)"""
        
        generated = hth.row_template(self.prof1["goals_scored"], self.prof2["goals_scored"],
                         "Goals")
        self.assertIn("<td class='values p2 text-success bg-success'>", generated)
    
    def test_row_template_p1_lt_p2_2(self):
        """player 1 has a 'smaller' value than player 2, but this time on an attribute like Price,
        where 'smaller' (cheaper) means better."""
        
        generated = hth.row_template(self.prof1["now_cost"], self.prof2["now_cost"], "Price", u"£", u"M")
        self.assertIn("<td class='values p1 text-success bg-success'", generated)
        self.assertIn("<td class='values p2'", generated)
    
    def test_row_template_p1_gt_p2(self):
        """player 1 has a greater value than player 2
        i.e. Mahrez has more points overall than Kane (as of gameweek 34)"""
        
        generated = hth.row_template(self.prof1["total_points"], self.prof2["total_points"],
                                         "Points")
        self.assertIn("<td class='values p1 text-success bg-success'>", generated)
    
    def test_row_template_p1_gt_p2_2(self):
        """Essentially it's test_row_template_p1_lt_p2_2 performed the other way around"""
        
        generated = hth.row_template(self.prof2["now_cost"], self.prof1["now_cost"], "Price", u"£", u"M")
        self.assertIn("<td class='values p2 text-success bg-success'", generated)
        self.assertIn("<td class='values p1'", generated)
    
    def test_row_template_p1_eq_p2(self):
        """Positive test. Pit player 1 (Mahrez) against himself to see if
        all of the rows are neutral."""
        
        generated = hth.row_template(self.prof1["assists"], self.prof1["assists"], "Assists")
        self.assertIn("<td class='values p1'>", generated)
        self.assertIn("<td class='values p2'>", generated)
    
    def test_generate_table(self):
        table = hth.generate_table(self.prof1, self.prof2)
        self.assertIn("<tr class='total_points'>", table)
        self.assertIn("<tr class='selected_by_percent'>", table)
        self.assertIn("<tr class='now_cost'>", table)
        self.assertIn("<tr class='goals_scored'>", table)
        self.assertIn("<tr class='assists'>", table)
        self.assertIn("<tr class='clean_sheets'>", table)
        self.assertIn("<tr class='yellow_cards'>", table)
        
    @classmethod
    def tearDownClass(cls):
        super(TestHeadToHead, cls).tearDownClass()
        cls.client.close()
        
if __name__ == "__main__":
    unittest.main()