import unittest
import pandas as pd
from utils.transform import clean_and_transform

class TestTransform(unittest.TestCase):

    def setUp(self):
        self.raw_data = pd.DataFrame([
            {
                "Title": "Valid Product",
                "Price": "$10.00",
                "Rating": "4.5",
                "Colors": "3 Colors",
                "Size": "M",
                "Gender": "Unisex"
            },
            {
                "Title": "Unknown Product",
                "Price": "$20.00",
                "Rating": "Invalid Rating",
                "Colors": "Unknown",
                "Size": "Size: L",
                "Gender": "Gender: Male"
            },
            {
                "Title": "Valid Product",  # Duplicate
                "Price": "$10.00",
                "Rating": "4.5",
                "Colors": "3 Colors",
                "Size": "M",
                "Gender": "Unisex"
            },
            {
                "Title": "Another Product",
                "Price": "$15.00",
                "Rating": "4.8 / 5",
                "Colors": "5 Colors",
                "Size": "L",
                "Gender": "Female"
            },
            {
                "Title": None,  # Null value
                "Price": "$30.00",
                "Rating": "5.0",
                "Colors": "2 Colors",
                "Size": "S",
                "Gender": "Unisex"
            }
        ])

    def test_clean_and_transform(self):
        cleaned_df = clean_and_transform(self.raw_data)

        # Cek hanya baris valid yang tersisa (2 baris)
        self.assertEqual(len(cleaned_df), 2)

        # Cek kolom dan tipe data
        expected_columns = ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'timestamp']
        self.assertListEqual(list(cleaned_df.columns), expected_columns)

        self.assertTrue(pd.api.types.is_object_dtype(cleaned_df['Title']))
        self.assertTrue(pd.api.types.is_float_dtype(cleaned_df['Price']))
        self.assertTrue(pd.api.types.is_float_dtype(cleaned_df['Rating']))
        self.assertTrue(pd.api.types.is_integer_dtype(cleaned_df['Colors']))
        self.assertTrue(pd.api.types.is_object_dtype(cleaned_df['Size']))
        self.assertTrue(pd.api.types.is_object_dtype(cleaned_df['Gender']))
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(cleaned_df['timestamp']))

        # Cek konversi harga
        price_values = cleaned_df['Price'].tolist()
        self.assertIn(160000.0, price_values)  # $10 * 16000
        self.assertIn(240000.0, price_values)  # $15 * 16000

if __name__ == '__main__':
    unittest.main()
