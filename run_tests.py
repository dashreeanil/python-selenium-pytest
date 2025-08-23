import subprocess
import time
import requests
import sys
import argparse
import os
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

# Configuration
DOCKER_COMPOSE_FILE = "docker-compose.yml"
GRID_URL = "http://localhost:4444/status"
GRID_CONTAINER = "selenium-hub"
SELENIUM_REMOTE_URL = "http://localhost:4444/wd/hub"
WAIT_TIMEOUT = 240  # seconds
RETRY_INTERVAL = 2  # seconds
MAX_SESSION_RETRIES = 3
DEFAULT_ALLURE_DIR = "reports/allure"

# Grid Management
def start_grid():
    print("🔧 Starting Selenium Grid via Docker Compose...")
    subprocess.run(["docker-compose", "-f", DOCKER_COMPOSE_FILE, "up", "-d"], check=True)

def check_container_health(container_name):
    try:
        result = subprocess.run(
            ["docker", "inspect", "--format='{{json .State.Health.Status}}'", container_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        status = result.stdout.strip().strip("'").replace('"', '')
        return status == "healthy"
    except Exception as e:
        print(f"⚠️ Health check failed: {e}")
        return False

def wait_for_grid():
    print("⏳ Waiting for Selenium Grid to be ready...")
    for _ in range(WAIT_TIMEOUT):
        try:
            response = requests.get(GRID_URL)
            if response.status_code == 200 and response.json().get("ready", False):
                if check_container_health(GRID_CONTAINER):
                    print("✅ Selenium Grid is ready and healthy.")
                    return
                else:
                    print("⚠️ Grid is ready but container health is not OK.")
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(RETRY_INTERVAL)
    print("❌ Grid did not become ready or healthy in time.")
    sys.exit(1)

def stop_grid():
    print("🧹 Stopping Selenium Grid...")
    subprocess.run(["docker-compose", "-f", DOCKER_COMPOSE_FILE, "down"], check=True)

# Browser Session Check
def verify_browser_session(browser, headless):
    print("🔁 Verifying browser session creation...")
    for attempt in range(1, MAX_SESSION_RETRIES + 1):
        try:
            options = None
            if browser == "chrome":
                options = webdriver.ChromeOptions()
            elif browser == "firefox":
                options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument("--headless")

            driver = webdriver.Remote(command_executor=SELENIUM_REMOTE_URL, options=options)
            driver.get("https://www.example.com")
            print(f"✅ Browser session successful on attempt {attempt}")
            driver.quit()
            return True
        except WebDriverException as e:
            print(f"⚠️ Attempt {attempt} failed: {e}")
            time.sleep(RETRY_INTERVAL)
    print("❌ Failed to create browser session after retries.")
    return False

# Pytest Execution
def prepare_allure_report_dir(path=DEFAULT_ALLURE_DIR):
    os.makedirs(path, exist_ok=True)
    return path

def build_pytest_command(env, browser, headless, markers, workers, allure_dir):
    cmd = ["pytest", "-n", str(workers), "--grid", f"--alluredir={allure_dir}"]
    if headless:
        cmd.append("--headless")
    if env:
        cmd.extend(["--environment", env])
    if browser:
        cmd.extend(["-o", f"browser={browser}"])
    if markers:
        cmd.extend(["-m", markers])
    return cmd

def run_pytest(cmd):
    print(f"🚀 Running tests: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode

def launch_allure_report(allure_dir=DEFAULT_ALLURE_DIR):
    print("📊 Generating and launching Allure report...")
    subprocess.run(["allure", "serve", allure_dir])

# CLI
def parse_args():
    parser = argparse.ArgumentParser(description="Run Selenium tests with Dockerized Grid and Allure")
    parser.add_argument("--env", default="qa", help="Environment to test (dev, qa, staging, prod)")
    parser.add_argument("--browser", choices=["chrome", "firefox"], default="chrome", help="Browser to use")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--markers", help="Run tests with specific pytest markers")
    parser.add_argument("--workers", type=int, default=4, help="Number of parallel pytest workers")
    parser.add_argument("--report", action="store_true", help="Launch Allure report after test run")
    return parser.parse_args()

# Main
if __name__ == "__main__":
    args = parse_args()
    allure_dir = prepare_allure_report_dir()

    try:
        start_grid()
        wait_for_grid()
        if not verify_browser_session(args.browser, args.headless):
            print("🛑 Aborting test run due to browser session failure.")
            stop_grid()
            sys.exit(1)

        pytest_cmd = build_pytest_command(args.env, args.browser, args.headless, args.markers, args.workers, allure_dir)
        exit_code = run_pytest(pytest_cmd)

        if exit_code == 0 and args.report:
            launch_allure_report(allure_dir)
    finally:
        stop_grid()
    sys.exit(exit_code)