from utils.logger_utility import logger
from utils.web_utility import WebUtility
from utils.api_utility import ApiUtility   
from utils.random_data_utility import RandomDataUtility

class BasePage:
    """
    Base class for all page objects, providing common functionality.
    """

    def __init__(self, driver):
        """
        Initialize the base page with a WebDriver instance.
        Args:
            driver (WebDriver): Selenium WebDriver instance.
        """
        self.driver = driver
        self.logger = logger
        self.web_utility = WebUtility(driver)
        self.api_utility = ApiUtility()
        self.random_data_utility = RandomDataUtility()
        
