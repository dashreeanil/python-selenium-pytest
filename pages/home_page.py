from pages.base_page import BasePage
from locators.home_page_locators import HomePageLocators

class HomePage(BasePage, HomePageLocators):

    def __init__(self, driver):
        """
        Initialize the HomePage with a WebDriver instance.
        Args:
            driver (WebDriver): Selenium WebDriver instance.
        """
        super().__init__(driver)

    def click_home_link(self):
        """
        Click the Home link on the home page.
        """
        self.logger.info("Clicking the Home link.")
        self.web_utility.click(self.HOME_LINK)
    
    def click_cart_link(self):
        """
        Click the Cart link on the home page.
        """
        self.logger.info("Clicking the Cart link.")
        self.web_utility.click(self.CART_LINK)

    def click_checkout_link(self):
        """
        Click the Checkout link on the home page.
        """
        self.logger.info("Clicking the Checkout link.")
        self.web_utility.click(self.CHECKOUT_LINK)

    def click_my_account_link(self):
        """
        Click the My Account link on the home page.
        """
        self.logger.info("Clicking the My Account link.")
        self.web_utility.click(self.MY_ACCOUNT_LINK)
    
    def click_sample_page_link(self):
        """
        Click the Sample Page link on the home page.
        """
        self.logger.info("Clicking the Sample Page link.")
        self.web_utility.click(self.SAMPLE_PAGE_LINK)

    def check_home_page_loaded(self):
        """
        Check if the home page has loaded by verifying the presence of the Home link.
        Returns:
            bool: True if the Home link is present, False otherwise.
        """
        self.logger.info("Checking if the home page has loaded.")
        return self.web_utility.is_visible(self.HOME_LINK)
    
    def validate_default_sorting(self):
        """
        Validate the default sorting of products on the home page.
        This method should be implemented based on the specific requirements of the application.
        Returns:
            bool: True if the default sorting is as expected, False otherwise.
        """
        self.logger.info("Validating default sorting of products on the home page.")
        # Placeholder for actual sorting validation logic
        titles = self.web_utility.find_elements(self.PRODUCT_TITLE)
        if not titles:
            self.logger.error("No product titles found on the home page.")
            return False    
        # Example logic: Check if titles are sorted alphabetically
        title_lst = []
        for title in titles:
            title_lst.append(self.web_utility.get_text_elements(title))
        if title_lst != sorted(title_lst):
            self.logger.error("Product titles are not sorted as expected.")
            return False    
       
        return True
    
    def search_product(self, product_name):
        """
        Search for a product by name on the home page.
        Args:
            product_name (str): The name of the product to search for.
        """
        self.logger.info(f"Searching for product: {product_name}")
        self.web_utility.send_keys_and_enter(self.SEARCH_FIELD, product_name)

    def assert_search_results(self, expected_product):
        """
        Assert that the search results contain the expected product.
        Args:
            expected_product (str): The name of the product expected in search results.
        Returns:
            bool: True if the expected product is found, False otherwise.
        """
        self.logger.info(f"Asserting search results for product: {expected_product}")
        actual_product_title = self.web_utility.get_text(self.SEARCHE_PRODUCT_TITLE)
        if expected_product.lower() in actual_product_title.lower():
            self.logger.info(f"Product '{expected_product}' found in search results.")
            return True 
        else:
            self.logger.error(f"Product '{expected_product}' not found in search results. Found: {actual_product_title}")
            return False
        
