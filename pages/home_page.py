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
        self.click(self.HOME_LINK)
    
    def click_cart_link(self):
        """
        Click the Cart link on the home page.
        """
        self.click(self.CART_LINK)

    def click_checkout_link(self):
        """
        Click the Checkout link on the home page.
        """
        self.click(self.CHECKOUT_LINK)

    def click_my_account_link(self):
        """
        Click the My Account link on the home page.
        """
        self.click(self.MY_ACCOUNT_LINK)
    
    def click_sample_page_link(self):
        """
        Click the Sample Page link on the home page.
        """
        self.click(self.SAMPLE_PAGE_LINK)
        
