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

    def enter_username(self, username):
        """
        Enter the username in the username text field.
        Args:
            username (str): The username to enter.
        """
        self.web_utility.send_keys(self.USERNAME_TEXT_FIELD, username)

    def enter_password(self, password):
        """
        Enter the password in the password text field.
        Args:
            password (str): The password to enter.
        """
        self.web_utility.send_keys(self.PASSWORD_TEXT_FIELD, password)

    def click_remember_me_checkbox(self):
        """
        Click the Remember Me checkbox.
        """
        self.web_utility.click(self.REMEMBER_ME_CHECKBOX)

    def click_login_button(self):
        """
        Click the Login button.
        """
        self.web_utility.click(self.LOGIN_BUTTON)   

    def click_lost_your_password_link(self):
        """
        Click the 'Lost your password?' link.
        """
        self.web_utility.click(self.LOST_YOUR_PASSWORD_LINK)

    def enter_register_email(self, email):
        """
        Enter the email in the registration email text field.
        Args:
            email (str): The email to enter for registration.
        """
        self.web_utility.send_keys(self.REGISTER_EMAIL_TEXT_FIELD, email)

    def enter_register_password(self, password):
        """
        Enter the password in the registration password text field.
        Args:
            password (str): The password to enter for registration.
        """
        self.web_utility.send_keys(self.REGISTER_PASSWORD_TEXT_FIELD, password)

    def click_register_button(self):
        """
        Click the Register button.
        """
        self.web_utility.click(self.REGISTER_BUTTON)

    def register_user(self, email, password):
        """
        Register a new user with the provided email and password.
        Args:
            email (str): The email to register.
            password (str): The password to register.
        """
        self.enter_register_email(email)
        self.enter_register_password(password)
        self.click_register_button()

    def login_user(self, username, password):
        """
        Log in a user with the provided username and password.
        Args:
            username (str): The username to log in.
            password (str): The password to log in.
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    def login_with_remember_me(self, username, password):
        """
        Log in a user with the provided username and password and remember me option.
        Args:
            username (str): The username to log in.
            password (str): The password to log in.
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_remember_me_checkbox()
        self.click_login_button() 

    def get_invalid_login_message(self):
        """
        Get the invalid login message displayed on the page.
        Returns:
            str: The invalid login message text.
        """
        return self.web_utility.get_text(self.INVALID_LOGIN_MESSAGE)

    def check_if_invalid_login_message_is_displayed(self,username, password,error_message):
        """
        Check if the invalid login message is displayed on the page.
        Args:
            username (str): The username to log in.
            password (str): The password to log in.
            error_message (str): The expected error message.
        """
        self.login_user(username, password)
        actual_message = self.get_invalid_login_message()
        assert actual_message == error_message, f"Expected '{error_message}', but got '{actual_message}'"
        

    


