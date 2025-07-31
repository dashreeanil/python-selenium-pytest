from selenium.webdriver.common.by import By
from utils.web_utility import WebUtility


class HomePageLocators(WebUtility):
    """A class for storing all locators for the home page."""

    HOME_LINK = (By.XPATH, "//a[.='Home']")
    CART_LINK = (By.XPATH, "//a[.='Cart']")
    CHECKOUT_LINK = (By.XPATH, "//a[.='Checkout']")
    MY_ACCOUNT_LINK = (By.XPATH, "//a[.='My account']")
    SAMPLE_PAGE_LINK = (By.XPATH, "//a[.='Sample Page']")



