import os
import pytest
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config", "config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def get_chrome_options(headless=False):
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
    options = FirefoxOptions()
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")
    if headless:
        options.add_argument("--headless")
    return options

def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", default=False, help="Run browsers in headless mode.")
    parser.addoption("--environment", action="store", default=None, help="Specify the environment (dev, qa, staging, prod).")
    parser.addoption("--grid", action="store_true", default=False, help="Run tests using Selenium Grid.")

@pytest.fixture(scope="session")
def config():
    return load_config()

@pytest.fixture(scope="function")
def init_driver(request, config):
    cli_env = request.config.getoption("--environment")
    cli_headless = request.config.getoption("--headless")
    use_grid = request.config.getoption("--grid")

    environment = cli_env if cli_env else config.get("environment", "dev")
    urls = config.get("urls", {})
    base_url = urls.get(environment)
    browser = config.get("browser", "chrome")
    headless = cli_headless if cli_headless is not None else config.get("headless", False)

    driver = None

    if use_grid:
        grid_url = config.get("grid_url", "http://localhost:4444/wd/hub")
        if browser == "chrome":
            options = get_chrome_options(headless)
            capabilities = DesiredCapabilities.CHROME.copy()
            capabilities["goog:chromeOptions"] = {"args": options.arguments}
        elif browser == "firefox":
            options = get_firefox_options(headless)
            capabilities = DesiredCapabilities.FIREFOX.copy()
            capabilities["moz:firefoxOptions"] = {"args": options.arguments}
        else:
            raise ValueError(f"Unsupported browser for Grid: {browser}")
        driver = webdriver.Remote(command_executor=grid_url, desired_capabilities=capabilities)
    else:
        if browser == "chrome":
            driver = webdriver.Chrome(options=get_chrome_options(headless))
        elif browser == "firefox":
            driver = webdriver.Firefox(options=get_firefox_options(headless))
        else:
            raise ValueError(f"Unsupported browser: {browser}")

    driver.implicitly_wait(10)
    driver.maximize_window()

    # Attach driver to test instance if using class-based tests
    if hasattr(request.node, "cls"):
        request.node.cls.driver = driver

    if base_url:
        driver.get(base_url)

    yield driver
    driver.quit()

@pytest.fixture(scope="session", autouse=True)
def create_screenshot_dir():
    if not os.path.exists("screenshot"):
        os.makedirs("screenshot")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = getattr(item.instance, "driver", None)
        if driver:
            test_case = item.parent.name if hasattr(item, "parent") else "unknown_case"
            test_step = item.name
            filename = f"screenshot/{test_case}_{test_step}.png"
            driver.save_screenshot(filename)