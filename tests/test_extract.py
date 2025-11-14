from unittest import TestCase
from unittest.mock import patch, MagicMock
import requests 
from bs4 import BeautifulSoup
from utils.extract import fetching_content, extract_product_data, scrape_products

class TestExtract(TestCase):

    def setUp(self):
        self.fake_html_page_1 = """
        <html><body>
            <div class="collection-card">
                <div class="product-details">
                    <h3 class="product-title">Fake T-Shirt</h3>
                    <div class="price-container"><span class="price">$100.00</span></div>
                    <p>Rating: ⭐ 4.0 / 5</p>
                    <p>3 Colors</p>
                    <p>Size: M</p>
                    <p>Gender: Men</p>
                </div>
            </div>
            <div class="collection-card">
                <div class="product-details">
                    <h3 class="product-title">Fake Hoodie</h3>
                    <div class="price-container"><span class="price">$200.00</span></div>
                    <p>Rating: ⭐ 5.0 / 5</p>
                    <p>5 Colors</p>
                    <p>Size: L</p>
                    <p>Gender: Unisex</p>
                </div>
            </div>
        </body></html>
        """
        self.fake_html_page_2 = "<html><body></body></html>"
        
        self.fake_html_price_unavailable = """
        <html><body>
            <div class="collection-card">
                <div class="product-details">
                    <h3 class="product-title">Pants 46</h3>
                    <p class="price">Price Unavailable</p> 
                    <p>Rating: Not Rated</p>
                    <p>8 Colors</p>
                    <p>Size: S</p>
                    <p>Gender: Men</p>
                </div>
            </div>
        </body></html>
        """

    @patch('utils.extract.requests.Session')
    def test_fetching_content_success(self, mock_session):
        mock_get = MagicMock()
        mock_get.content = b"Success HTML"
        mock_session.return_value.get.return_value = mock_get
        
        result = fetching_content("http://fake-url.com")
        
        self.assertEqual(result, b"Success HTML")
        mock_get.raise_for_status.assert_called_once()

    @patch('utils.extract.requests.Session')
    def test_fetching_content_http_error(self, mock_session):
        mock_get = MagicMock()
        mock_get.raise_for_status.side_effect = requests.exceptions.RequestException("Test 404 Error")
        mock_session.return_value.get.return_value = mock_get
        
        result = fetching_content("http://fake-url.com")
        
        self.assertIsNone(result)

    def test_extract_product_data_success(self):
        soup = BeautifulSoup(self.fake_html_page_1, "html.parser")
        card = soup.find('div', class_='collection-card')
        
        product = extract_product_data(card)
        
        self.assertEqual(product['Title'], 'Fake T-Shirt')
        self.assertEqual(product['Price'], '$100.00')
        self.assertEqual(product['Rating'], 'Rating: ⭐ 4.0 / 5')
        self.assertEqual(product['Colors'], '3 Colors')
        self.assertEqual(product['Size'], 'Size: M')
        self.assertEqual(product['Gender'], 'Gender: Men')
        self.assertIn('timestamp', product)

    def test_extract_product_data_unavailable(self):
        soup = BeautifulSoup(self.fake_html_price_unavailable, "html.parser")
        card = soup.find('div', class_='collection-card')
        
        product = extract_product_data(card)
        
        self.assertEqual(product['Title'], 'Pants 46')
        self.assertEqual(product['Price'], 'Price Unavailable')
        self.assertEqual(product['Rating'], 'Rating: Not Rated')

    @patch('utils.extract.fetching_content')
    def test_scrape_products_loop(self, mock_fetching_content):
        responses = [self.fake_html_page_1, self.fake_html_page_2]
        mock_fetching_content.side_effect = responses + [None] * 48
        
        data = scrape_products(delay=0)

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['Title'], 'Fake T-Shirt')
        self.assertEqual(data[1]['Title'], 'Fake Hoodie')
        
        self.assertEqual(mock_fetching_content.call_count, 2)

    @patch('utils.extract.fetching_content')
    def test_scrape_products_fetch_fails_and_continues(self, mock_fetching_content):
        mock_card = BeautifulSoup(self.fake_html_page_1, "html.parser").find('div', class_='collection-card')
        fake_page_one_product = f"<html><body>{mock_card}</body></html>"
        
        responses = [None, fake_page_one_product, self.fake_html_page_2]
        mock_fetching_content.side_effect = responses + [None] * 47
        
        data = scrape_products(delay=0)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['Title'], 'Fake T-Shirt')
        
        self.assertEqual(mock_fetching_content.call_count, 3)