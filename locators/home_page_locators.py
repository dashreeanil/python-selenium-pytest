from selenium.webdriver.common.by import By
from utils.web_utility import WebUtility


class HomePageLocators(WebUtility):
    """A class for storing all locators for the home page."""

    HOME_LINK = (By.XPATH, "//div[@class = 'menu']/ul[@class='nav-menu']//a[.='Home']")
    CART_LINK = (By.XPATH, "//div[@class = 'menu']/ul[@class='nav-menu']//a[.='Cart']")
    CHECKOUT_LINK = (By.XPATH, "//div[@class = 'menu']/ul[@class='nav-menu']//a[.='Checkout']")
    MY_ACCOUNT_LINK = (By.XPATH, "//div[@class = 'menu']/ul[@class='nav-menu']//a[.='My Account']")
    SAMPLE_PAGE_LINK = (By.XPATH, "//div[@class = 'menu']/ul[@class='nav-menu']//a[.='Sample Page']")



