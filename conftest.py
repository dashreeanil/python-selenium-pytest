import os
import pytest
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import datetime


def load_config():
    """
    Load the configuration from config/config.yaml file.
    Returns:
        dict: Configuration data loaded from YAML.
    """
    config_path = os.path.join(os.path.dirname(__file__), "config", "config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def get_chrome_options(headless=False):
    """
    Get Chrome WebDriver options.
    Args:
        headless (bool): Whether to run Chrome in headless mode.
    Returns:
        ChromeOptions: Configured Chrome options.
    """
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    if headless:
        options.add_argument("--headless=new")
    return options

def get_firefox_options(headless=False):
    """
    Get Firefox WebDriver options.
    Args:
        headless (bool): Whether to run Firefox in headless mode.
    Returns:
        FirefoxOptions: Configured Firefox options.
    """
    options = FirefoxOptions()
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")
    if headless:
        options.add_argument("--headless")
    return options

def pytest_addoption(parser):
    """
    Add custom command line options to pytest.
    Args:
        parser: Pytest parser object.
    """
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browsers in headless mode."
    )
    parser.addoption(
        "--environment",
        action="store",
        default=None,
        help="Specify the environment to run tests against (dev, qa, staging, prod)."
    )

@pytest.fixture(scope="session")
def config():
    """
    Pytest fixture to load configuration once per test session.
    Returns:
        dict: Configuration data.
    """
    return load_config()

@pytest.fixture(scope="class")
def init_driver(request, config):
    """
    Pytest fixture to initialize the WebDriver based on config and command line options.
    Sets the driver as a class attribute and navigates to the environment-specific base URL.
    Yields:
        WebDriver: Selenium WebDriver instance.
    """
    # Read environment and headless from command line, fallback to config.yaml
    cli_env = request.config.getoption("--environment")
    cli_headless = request.config.getoption("--headless")
    environment = cli_env if cli_env else config.get("environment", "dev")
    urls = config.get("urls", {})
    base_url = urls.get(environment)
    browser = config.get("browser", "chrome")
    # Command line --headless overrides config.yaml
    headless = cli_headless if cli_headless is not None else config.get("headless", False)

    if browser == "chrome":
        driver = webdriver.Chrome(options=get_chrome_options(headless))
    elif browser == "firefox":
        driver = webdriver.Firefox(options=get_firefox_options(headless))
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    driver.implicitly_wait(10)  # Set implicit wait for elements
    driver.maximize_window()  # Maximize the browser window
    request.cls.driver = driver

    # Launch browser to environment-specific base_url if provided
    if base_url:
        driver.get(base_url)

    yield driver
    driver.quit()



@pytest.fixture(scope="session", autouse=True)
def create_screenshot_dir():
    """
    Pytest fixture to create a screenshot directory before the test session starts.
    """
    if not os.path.exists("screenshot"):
        os.makedirs("screenshot")

def pytest_configure(config):
    global pytest_html
    pytest_html = config.pluginmanager.getplugin("html")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Access the test class instance
        test_class_instance = item.instance
        driver = getattr(test_class_instance, "driver", None)

        if driver:
            screenshot_dir = os.path.abspath("screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"{item.name}_{timestamp}.png"
            file_path = os.path.join(screenshot_dir, file_name)
            driver.save_screenshot(file_path)
            is_frontend = True if 'init_driver' in item.fixturenames else False
            if is_frontend:
                extra = getattr(report, 'extra', [])
                extra.append(pytest_html.extras.image(file_path))
                report.extra = extra


