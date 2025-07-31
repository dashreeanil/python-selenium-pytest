from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import allure
from utils.logger_utility import logger

class WebUtility:
    def __init__(self, driver, timeout=10):
        """
        Initialize WebUtility with a Selenium WebDriver instance and optional timeout.
        """
        self.driver = driver
        self.timeout = timeout

    @allure.step("Navigate to URL: {1}")
    def go_to(self, url):
        """
        Navigate to the specified URL and wait for the page to load.
        """
        try:
            logger.info(f"Navigating to URL: {url}")
            self.driver.get(url)
            WebDriverWait(self.driver, self.timeout).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
        except Exception as e:
            logger.error(f"Failed to navigate to URL {url}: {e}")
            allure.attach(str(e), name="Navigation Error", attachment_type=allure.attachment_type.TEXT)
            raise
        return self

    @allure.step("Find element by {1}: {2}")
    def find_element(self, locator):
        """
        Find a single element using the given locator strategy and value.
        """
        try:
            logger.debug(f"Finding element by locator: {locator}")
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except Exception as e:
            logger.error(f"Failed to find element by locator: {locator} - {e}")
            allure.attach(str(e), name="Find Element Error", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Find elements by locator: {locator}")
    def find_elements(self, locator: tuple):
        """
        Find multiple elements using the given locator strategy and value.
        """
        try:
            logger.debug(f"Finding elements by locator: {locator}")
            elements = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except Exception as e:
            logger.error(f"Failed to find elements by locator: {locator} - {e}")
            allure.attach(str(e), name="Find Elements Error", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Click element by locator: {locator}")
    def click(self, locator: tuple):
        """
        Click on an element after waiting for it to be clickable.
        """
        try:
            logger.info(f"Clicking element by locator: {locator}")
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
        except Exception as e:
            logger.error(f"Failed to click element by locator: {locator} - {e}")
            allure.attach(str(e), name="Click Error", attachment_type=allure.attachment_type.TEXT)
            raise
        return self

    @allure.step("Send keys '{keys}' to element {locator}")
    def send_keys(self, locator: tuple, keys: str):
        """
        Send keys to an element after waiting for it to be visible.

        :param locator: Tuple of (By, locator_value)
        :param keys: String to type into the element
        """
        try:
            logger.info(f"Sending keys '{keys}' to element located by {locator}")
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
            element.clear()
            element.send_keys(keys)
        except Exception as e:
            logger.error(f"Failed to send keys to element {locator} - {e}")
            allure.attach(str(e), name="Send Keys Error", attachment_type=allure.attachment_type.TEXT)
            raise
        return self

    @allure.step("Get text from element by {locator}")
    def get_text(self, locator: tuple):
        """
        Get the text of an element after waiting for it to be visible.
        """
        try:
            logger.debug(f"Getting text from element by locator: {locator}")
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
            text = element.text
            logger.info(f"Text found: {text}")
            return text
        except Exception as e:
            logger.error(f"Failed to get text from element by locator: {locator} - {e}")
            allure.attach(str(e), name="Get Text Error", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Wait for element to be clickable by locator: {locator}")
    def wait_for_clickable(self, locator: tuple):
        """
        Wait for an element to be clickable and return it.
        """
        try:
            logger.debug(f"Waiting for element to be clickable by locator: {locator}")
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except Exception as e:
            logger.error(f"Element not clickable by locator: {locator} - {e}")
            allure.attach(str(e), name="Wait Clickable Error", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Check if element is visible by locator: {locator}")
    def is_visible(self, locator: tuple):
        """
        Check if an element is visible on the page.
        """
        try:
            logger.debug(f"Checking visibility for element by locator: {locator}")
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
            logger.info("Element is visible.")
            return True
        except Exception as e:
            logger.warning(f"Element not visible by locator: {locator} - {e}")
            allure.attach(str(e), name="Visibility Error", attachment_type=allure.attachment_type.TEXT)
            return False

    @allure.step("Get attribute '{2}' from element by locator: {locator}")
    def get_attribute(self, locator: tuple, attribute):
        """
        Get the value of an attribute from an element.
        """
        try:
            logger.debug(f"Getting attribute '{attribute}' from element by locator: {locator}")
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(locator)
            )
            attr_value = element.get_attribute(attribute)
            logger.info(f"Attribute value: {attr_value}")
            return attr_value
        except Exception as e:
            logger.error(f"Failed to get attribute '{attribute}' from element by locator: {locator} - {e}")
            allure.attach(str(e), name="Get Attribute Error", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Switch to frame by locator: {locator}")
    def switch_to_frame(self, locator: tuple):
        """
        Switch to a frame using the given locator.
        """
        try:
            logger.info(f"Switching to frame by locator: {locator}")
            frame = WebDriverWait(self.driver, self.timeout).until(
                EC.frame_to_be_available_and_switch_to_it(locator)
            )
        except Exception as e:
            logger.error(f"Failed to switch to frame by locator: {locator} - {e}")
            allure.attach(str(e), name="Switch Frame Error", attachment_type=allure.attachment_type.TEXT)
            raise
        return self

    @allure.step("Switch to default content")
    def switch_to_default_content(self):
        """
        Switch to the default content from any frame.
        """
        try:
            logger.info("Switching to default content")
            self.driver.switch_to.default_content()
        except Exception as e:
            logger.error(f"Failed to switch to default content - {e}")
            allure.attach(str(e), name="Switch Default Content Error", attachment_type=allure.attachment_type.TEXT)
            raise
        return self

    @allure.step("Accept alert")
    def accept_alert(self):
        """
        Accept a browser alert if present.
        """
        try:
            logger.info("Accepting alert")
            WebDriverWait(self.driver, self.timeout).until(EC.alert_is_present())
            self.driver.switch_to.alert.accept()
        except Exception as e:
            logger.error(f"Failed to accept alert - {e}")
            allure.attach(str(e), name="Accept Alert Error", attachment_type=allure.attachment_type.TEXT)
            raise
        return self

    @allure.step("Dismiss alert")
    def dismiss_alert(self):
        """
        Dismiss a browser alert if present.
        """
        try:
            logger.info("Dismissing alert")
            WebDriverWait(self.driver, self.timeout).until(EC.alert_is_present())
            self.driver.switch_to.alert.dismiss()
        except Exception as e:
            logger.error(f"Failed to dismiss alert - {e}")
            allure.attach(str(e), name="Dismiss Alert Error", attachment_type=allure.attachment_type.TEXT)
            raise
        return self

    @allure.step("Refresh page")
    def refresh(self):
        """
        Refresh the current page and wait for it to load.
        """
        try:
            logger.info("Refreshing page")
            self.driver.refresh()
            WebDriverWait(self.driver, self.timeout).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
        except Exception as e:
            logger.error(f"Failed to refresh page - {e}")
            allure.attach(str(e), name="Refresh Error", attachment_type=allure.attachment_type.TEXT)
            raise
        return self

    @allure.step("Perform action chain")
    def perform_action_chain(self, actions_callback):
        """
        Perform a custom ActionChains sequence using the provided callback.
        The callback should accept an ActionChains object and perform actions on it.
        """
        try:
            logger.info("Performing action chain")
            actions = ActionChains(self.driver)
            actions_callback(actions)
            actions.perform()
        except Exception as e:
            logger.error(f"Failed to perform action chain - {e}")
            allure.attach(str(e), name="Action Chain Error", attachment_type=allure.attachment_type.TEXT)
            raise
        return self

    @allure.step("Select option in dropdown by {1}: {2} using {3}='{4}'")
    def select_dropdown(self, by, value, select_by="value", option=""):
        """
        Select an option in a dropdown using value, visible text, or index.
        """
        try:
            logger.info(f"Selecting dropdown option by {by}: {value} using {select_by}='{option}'")
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            select = Select(element)
            if select_by == "value":
                select.select_by_value(option)
            elif select_by == "visible_text":
                select.select_by_visible_text(option)
            elif select_by == "index":
                select.select_by_index(int(option))
            else:
                raise ValueError(f"Invalid select_by: {select_by}")
        except Exception as e:
            logger.error(f"Failed to select dropdown option by {by}: {value} - {e}")
            allure.attach(str(e), name="Select Dropdown Error", attachment_type=allure.attachment_type.TEXT)
            raise
        return self

    @allure.step("Context click (right click) on element by {1}: {2}")
    def context_click(self, by, value):
        """
        Perform a context (right) click on the specified element.
        """
        try:
            logger.info(f"Performing context click on element by {by}: {value}")
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            actions = ActionChains(self.driver)
            actions.context_click(element).perform()
        except Exception as e:
            logger.error(f"Failed to context click on element by {by}: {value} - {e}")
            allure.attach(str(e), name="Context Click Error", attachment_type=allure.attachment_type.TEXT)
            raise
        return self

    @allure.step("Mouse hover on element by {1}: {2}")
    def mouse_hover(self, by, value):
        """
        Perform a mouse hover over the specified element.
        """
        try:
            logger.info(f"Performing mouse hover on element by {by}: {value}")
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
        except Exception as e:
            logger.error(f"Failed to mouse hover on element by {by}: {value} - {e}")
            allure.attach(str(e), name="Mouse Hover Error", attachment_type=allure.attachment_type.TEXT)
            raise
        return self