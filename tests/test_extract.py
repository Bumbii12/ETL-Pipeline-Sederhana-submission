import unittest
from bs4 import BeautifulSoup
from utils.extract import extract_fashion_data

class TestExtractFashionData(unittest.TestCase):
    def setUp(self):
        """Setup HTML sample for testing."""
        self.html = """
        <div class="collection-card">
            <div class="product-details">
                <h3 class="product-title">Test Product</h3>
                <div class="price-container"><span class="price">$123.45</span></div>
                <p style="font-size: 14px; color: #777;">Rating: ⭐ 4.5 / 5</p>
                <p style="font-size: 14px; color: #777;">5 Colors</p>
                <p style="font-size: 14px; color: #777;">Size: M</p>
                <p style="font-size: 14px; color: #777;">Gender: Unisex</p>
            </div>
        </div>
        """
        self.soup = BeautifulSoup(self.html, "html.parser")
        self.article = self.soup.find('div', class_='collection-card')

    def test_extract_fashion_data(self):
        """Test extracting fashion data from a single article."""
        expected_data = {
            "Title": "Test Product",
            "Price": "$123.45",
            "Rating": "4.5",
            "Colors": "5",
            "Size": "M",
            "Gender": "Unisex"
        }
        extracted_data = extract_fashion_data(self.article)
        self.assertEqual(extracted_data, expected_data)

    def test_extract_fashion_data_missing_fields(self):
        """Test extracting data when some fields are missing."""
        incomplete_html = """
        <div class="collection-card">
            <div class="product-details">
                <h3 class="product-title">Incomplete Product</h3>
                <div class="price-container"><span class="price">$99.99</span></div>
            </div>
        </div>
        """
        soup = BeautifulSoup(incomplete_html, "html.parser")
        article = soup.find('div', class_='collection-card')
        expected_data = {
            "Title": "Incomplete Product",
            "Price": "$99.99",
            "Rating": "Not Rated",
            "Colors": "Unknown",
            "Size": "Unknown",
            "Gender": "Unknown"
        }
        extracted_data = extract_fashion_data(article)
        self.assertEqual(extracted_data, expected_data)

if __name__ == '__main__':
    unittest.main()