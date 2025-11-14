import pandas as pd
import numpy as np
from unittest import TestCase
from utils.transform import transform_data

class TestTransform(TestCase):

    def setUp(self):
        self.dummy_dirty_data = [
            {'Title': 'T-shirt 2', 'Price': '$102.15', 'Rating': 'Rating: ⭐ 3.9 / 5', 'Colors': '3 Colors', 'Size': 'Size: M', 'Gender': 'Gender: Women', 'timestamp': '...'},
            {'Title': 'Hoodie 3', 'Price': '$496.88', 'Rating': 'Rating: ⭐ 4.8 / 5', 'Colors': '3 Colors', 'Size': 'Size: L', 'Gender': 'Gender: Unisex', 'timestamp': '...'},
            
            {'Title': 'Unknown Product', 'Price': '$100.00', 'Rating': 'Rating: ⭐ 4.0 / 5', 'Colors': '5 Colors', 'Size': 'Size: M', 'Gender': 'Gender: Men', 'timestamp': '...'}, # Invalid Title
            {'Title': 'Jacket 5', 'Price': 'Price Unavailable', 'Rating': 'Rating: ⭐ 3.5 / 5', 'Colors': '3 Colors', 'Size': 'Size: XXL', 'Gender': 'Gender: Women', 'timestamp': '...'}, # Invalid Price
            {'Title': 'Jacket 6', 'Price': '$200.00', 'Rating': 'Not Rated', 'Colors': '3 Colors', 'Size': 'Size: S', 'Gender': 'Gender: Unisex', 'timestamp': '...'}, # Invalid Rating 1
            {'Title': 'Jacket 7', 'Price': '$250.00', 'Rating': 'Rating: ⭐ Invalid Rating / 5', 'Colors': '3 Colors', 'Size': 'Size: S', 'Gender': 'Gender: Unisex', 'timestamp': '...'}, # Invalid Rating 2
            
            {'Title': 'Pants 4', 'Price': '$467.31', 'Rating': 'Rating: ⭐ 3.3 / 5', 'Colors': None, 'Size': 'Size: XL', 'Gender': 'Gender: Men', 'timestamp': '...'}, # Data Null
            
            {'Title': 'T-shirt 2', 'Price': '$102.15', 'Rating': 'Rating: ⭐ 3.9 / 5', 'Colors': '3 Colors', 'Size': 'Size: M', 'Gender': 'Gender: Women', 'timestamp': '...'} # Duplikat
        ]

    def test_transform_data_success(self):
        cleaned_df = transform_data(self.dummy_dirty_data)
        
        self.assertIsInstance(cleaned_df, pd.DataFrame)
        self.assertEqual(len(cleaned_df), 2)
        
        self.assertEqual(cleaned_df['Price'].dtype, 'float64')
        self.assertEqual(cleaned_df['Rating'].dtype, 'float64')
        self.assertEqual(cleaned_df['Colors'].dtype, 'int64')
        
        self.assertEqual(cleaned_df['Price'].iloc[0], 1634400.0)
        
        self.assertEqual(cleaned_df['Size'].iloc[0], 'M')
        self.assertEqual(cleaned_df['Gender'].iloc[0], 'Women')
        self.assertIn('timestamp', cleaned_df.columns)

    def test_transform_data_empty_input(self):
        cleaned_df = transform_data([])
        self.assertTrue(cleaned_df.empty)

    def test_transform_data_all_dirty(self):
        all_dirty_data = [
            {'Title': 'Unknown Product', 'Price': '$100.00', 'Rating': 'Rating: ⭐ 4.0 / 5', 'Colors': '5 Colors', 'Size': 'Size: M', 'Gender': 'Gender: Men', 'timestamp': '...'},
            {'Title': 'Jacket 5', 'Price': 'Price Unavailable', 'Rating': 'Rating: ⭐ 3.5 / 5', 'Colors': '3 Colors', 'Size': 'Size: XXL', 'Gender': 'Gender: Women', 'timestamp': '...'}
        ]
        
        cleaned_df = transform_data(all_dirty_data)
        
        self.assertTrue(cleaned_df.empty)

    def test_transform_data_exception(self):
        cleaned_df = transform_data(None)
        self.assertTrue(cleaned_df.empty)