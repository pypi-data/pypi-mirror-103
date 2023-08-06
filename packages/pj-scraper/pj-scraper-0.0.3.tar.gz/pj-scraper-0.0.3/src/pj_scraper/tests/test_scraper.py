from unittest import TestCase
from unittest.mock import patch

import bs4
import pandas as pd

from pj_scraper.scraper import Scraper


class TestScraper(TestCase):
    def test_dummy(self):
        assert True

    @patch("requests.get")
    @patch("bs4.BeautifulSoup")
    def test_get_soup(self, mock_bs4, mock_req):
        """ Test initialization of soup """
        s = Scraper()
        s._get_soup("some_url")
        mock_req.assert_called_with("some_url")
        mock_bs4.assert_called()

    def test_get_products(self):
        """ Test that correct info is gathered from a page """
        dummy_request_content = '<a aria-label="Apple iPhone 12 64GB" class="ProductLink-sc-882dpj-1 kHbpTA" href="/product.php?p=5594641"><a aria-label="Apple iPhone 12 64GB" class="ProductLink-sc-882dpj-1 kHbpTA" href="/product.php?p=5594641">'
        dummy_soup = bs4.BeautifulSoup(dummy_request_content)

        s = Scraper()
        products = s.get_products_from_page(dummy_soup)

        self.assertEqual(products.loc[0, "product_name"], "Apple iPhone 12 64GB")
        self.assertEqual(products.loc[1, "product_number"], "5594641")

    @patch("pj_scraper.scraper.Scraper._get_soup")
    @patch("pj_scraper.scraper.Scraper.get_products_from_page")
    def test_all_prods_from_category(self, mock_get_prods, mock_get_soup):
        """ """

        s = Scraper()
        cat = "some_category"

        mock_get_prods.return_value = pd.DataFrame(
            {"product_name": ["product"], "product_number": ["1234"]}
        )
        prods = s.get_all_products_from_category(cat, no_pages=2)
        self.assertEqual(len(prods), 2)
        self.assertEqual(prods.iloc[0]["category"], cat)

    @patch("pj_scraper.scraper.Scraper._get_soup")
    def test_get_sellers_and_prices_of_product(self, mock_get_soup):

        dummy_response = '<script data-script="foo"></script><script data-script="globals">,{"__typename":"Price","id":"4428260864","name":"ASUS ROG STRIX Z590-F GAMING WIFI ATX LGA1200 Intel Z590","type":"normal","externalUri":null,"stock":{"status":"in_stock","statusText":"200 p\xE5 lager"},"deliveryOptions":[],"authorizedBy":[],"price":{"inclShipping":null,"exclShipping":3500,"originalCurrency":"NOK","originalCurrencyExclShipping":"3500"},"store":{"id":37622,"name":"Invensys","featured":false,"hasLogo":false,"logo":null,"pathName":"/shop.php?f=37622","providedByStore":{"generalInformation":null},"userReviewSummary":{"rating":null,"count":0,"countTotal":0},"market":"primary","marketplace":false,"countryCode":"no","primaryMarket":"no","currency":"NOK"},"brandRecommendedRetailer":false,"alternativePrices":[{"__typename":"AlternativePrice","id":"4428260864","name":"ASUS ROG STRIX Z590-F GAMING WIFI ATX LGA1200 Intel Z590","type":"normal","externalUri":null,"stock":{"status":"in_stock","statusText":"200 p\xE5 lager"},"price":{"exclShipping":3500,"inclShipping":null,"originalCurrency":"NOK","originalCurrencyExclShipping":"3500"}},{"__typename":"AlternativePrice","id":"4184620430","name":"ASUS ROG STRIX Z590-F GAMING WIFI (ATX, Z590, LGA 1200)","type":null,"externalUri":null,"stock":{"status":"in_stock","statusText":"4 p\xE5 lager"},"price":{"exclShipping":3795,"inclShipping":null,"originalCurrency":"NOK","originalCurrencyExclShipping":null}}],"variants":null},{"__typename":"Price","id":"4428260864","name":"ASUS ROG STRIX Z590-F GAMING WIFI ATX LGA1200 Intel Z590","type":"normal","externalUri":null,"stock":{"status":"in_stock","statusText":"200 p\xE5 lager"},"deliveryOptions":[],"authorizedBy":[],"price":{"inclShipping":null,"exclShipping":3500,"originalCurrency":"NOK","originalCurrencyExclShipping":"3500"},"store":{"id":37622,"name":"Invensys","featured":false,"hasLogo":false,"logo":null,"pathName":"/shop.php?f=37622","providedByStore":{"generalInformation":null},"userReviewSummary":{"rating":null,"count":0,"countTotal":0},"market":"primary","marketplace":false,"countryCode":"no","primaryMarket":"no","currency":"NOK"},"brandRecommendedRetailer":false,"alternativePrices":[{"__typename":"AlternativePrice","id":"4428260864","name":"ASUS ROG STRIX Z590-F GAMING WIFI ATX LGA1200 Intel Z590","type":"normal","externalUri":null,"stock":{"status":"in_stock","statusText":"200 p\xE5 lager"},"price":{"exclShipping":3500,"inclShipping":null,"originalCurrency":"NOK","originalCurrencyExclShipping":"3500"}},{"__typename":"AlternativePrice","id":"4184620430","name":"ASUS ROG STRIX Z590-F GAMING WIFI (ATX, Z590, LGA 1200)","type":null,"externalUri":null,"stock":{"status":"in_stock","statusText":"4 p\xE5 lager"},"price":{"exclShipping":3795,"inclShipping":null,"originalCurrency":"NOK","originalCurrencyExclShipping":null}}],"variants":null}</script>'
        mock_get_soup.return_value = bs4.BeautifulSoup(dummy_response)

        s = Scraper()
        prices = s.get_sellers_and_prices_of_product("1234")
        self.assertEqual(len(prices), 2)
        self.assertEqual(prices.iloc[0]["price_excl_shipping"], 3500)
