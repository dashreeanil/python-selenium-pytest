from selenium.webdriver.common.by import By
class MyAccountPage:
    """
    This class represents the My Account page.
    """

    USERNAME_TEXT_FIELD = (By.ID, "username")
    PASSWORD_TEXT_FIELD = (By.ID, "password")
    REMEMBER_ME_CHECKBOX = (By.ID, "rememberme")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[value='Log in']")
    LOST_YOUR_PASSWORD_LINK = (By.LINK_TEXT, "Lost your password?")
    REGISTER_EMAIL_TEXT_FIELD = (By.ID, "reg_email")
    REGISTER_PASSWORD_TEXT_FIELD = (By.ID, "reg_password")
    REGISTER_BUTTON = (By.CSS_SELECTOR, "button[name='register']")
    INVALID_LOGIN_MESSAGE = (By.CSS_SELECTOR, "ul[role='alert'] li")
    