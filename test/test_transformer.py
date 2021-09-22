import unittest
import os
import sys

current_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(current_dir + "/../web_scraping"))

import scraper
import transformer


class TestTransformer(unittest.TestCase):
    dfs = scraper.scrape("https://id.wikipedia.org/wiki/Daftar_orang_terkaya_di_Indonesia")
    new_df = transformer.transform([dfs[3], dfs[4], dfs[5], dfs[6], dfs[7]], [2011, 2013, 2017, 2019, 2020])
    
    
    def test_is_year_between_2011_and_2020(self, cleaned_df=new_df):
        actual = cleaned_df['tahun'].nunique()
        expected = 5
        
        self.assertEqual(actual, expected)
        
    
    def test_shape_of_dataframe(self, cleaned_df=new_df):
        actual = cleaned_df.shape
        expected = (218, 5)
        
        self.assertEqual(actual, expected)
        
    
    def test_is_money_miliar_when_string_money_contains_miliar(self):
        string_money = "35.5 miliar"
        actual = transformer.is_money_miliar(string_money)

        self.assertTrue(string_money)
    
    
    def test_is_money_miliar_when_string_money_not_contains_miliar(self):
        string_money = "980 juta"
        actual = transformer.is_money_miliar(string_money)

        self.assertFalse(actual)
    
    
    def test_transform_money_format_when_money_is_juta(self):
        string_money = "980 Juta"
        actual = transformer.transform_money_format(string_money)

        self.assertEqual(actual, "980")
    

    def test_transform_money_format_when_money_is_miliar(self):
        string_money = "35.5 Miliar"
        actual = transformer.transform_money_format(string_money)

        self.assertEqual(actual, "35.5")
    

    def test_transform_money_format_when_money_contains_comma(self):
        string_money = "35,5 Miliar"
        actual = transformer.transform_money_format(string_money)

        self.assertEqual(actual, "35.5")


if __name__ == "__main__":
    unittest.main()