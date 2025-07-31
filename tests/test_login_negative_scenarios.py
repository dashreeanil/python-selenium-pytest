from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from utils.helper_utility import HelperUtility
class TestLoginNegativeScenarios:
    """
    Test class for negative login scenarios.
    This class contains tests that verify the behavior of the login functionality
    when provided with invalid credentials or other erroneous inputs.
    """

    def test_login_with_invalid_username(self, init_driver):
        """
        Test case to verify login with an invalid username.
        """
        driver = init_driver
        data = HelperUtility.get_test_data("tc_001","my_account_page")
        print(f"Test Data: {data}")
        home_page = HomePage(driver)
        my_account_page = MyAccountPage(driver)
        home_page.click_my_account_link()
        my_account_page.login_user(data["username"], data["password"])
        error_message = my_account_page.get_invalid_login_message()
        assert data["error_message"] in error_message, "Expected error message not found."