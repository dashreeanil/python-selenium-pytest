from utils.logger_utility import logger
from utils.web_utility import WebUtility
from utils.api_utility import APIUtility   
from utils.random_data_utility import RandomDataUtility
from utils.helper_utility import HelperUtility

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
        self.timeout = self.web_utility.timeout 
        self.api_utility = APIUtility()
        self.random_data_utility = RandomDataUtility()
        self.helper = HelperUtility()
        
