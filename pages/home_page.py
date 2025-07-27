from pages.base_page import BasePage

class HomePage(BasePage):

    def __init__(self, driver):
        """
        Initialize the HomePage with a WebDriver instance.
        Args:
            driver (WebDriver): Selenium WebDriver instance.
        """
        super().__init__(driver)
        