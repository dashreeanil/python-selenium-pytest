from pages.base_page import BasePage
from locators.my_account_page_locators import MyAccountPageLocators

class MyAccountPage(BasePage,MyAccountPageLocators):
    """
    This class represents the My Account page.
    It inherits from BasePage and uses locators defined in MyAccountPageLocators.
    """

    def __init__(self, driver):
        """
        Initializes the MyAccountPage with the given WebDriver instance.
        Args:
            driver (WebDriver): Selenium WebDriver instance.
        """
        super().__init__(driver)
