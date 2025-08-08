from pages.home_page import HomePage
import pytest

class TestHomePageScenarios:
    """
    Test scenarios for the home page.
    """

    def test_home_page_loaded(self, init_driver):
        """
        Test to verify that the home page has loaded successfully.
        """
        home_page = HomePage(init_driver)
        assert home_page.check_home_page_loaded(), "Home page did not load successfully."

    def test_validate_default_sorting(self, init_driver):
        """
        Test to validate the default sorting of products on the home page.
        """
        home_page = HomePage(init_driver)
        home_page.click_home_link()
        # Assuming there is a method to validate default sorting
        assert home_page.validate_default_sorting(), "Default sorting is not as expected."

    @pytest.mark.parametrize("product_name", [
        "Album","Beanie","Belt","Hoodie","Polo"])
    def test_search_product(self, init_driver,product_name):
        """
        Test to search for a product on the home page.
        """
        home_page = HomePage(init_driver)
        home_page.click_home_link()
        home_page.search_product(product_name)
        home_page.assert_search_results(product_name)