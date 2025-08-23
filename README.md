# Selenium Pytest Automation Framework

A robust, scalable, and modular automation framework for UI, API, and database testing using Selenium, Pytest, and Python best practices.

## Features
- **Selenium WebDriver**: Supports Chrome, Firefox, and Selenium Grid execution
- **Pytest**: Simple, powerful test discovery and execution
- **Page Object Model (POM)**: Clean separation of page logic and test logic
- **API Testing**: Built-in utilities for REST API validation
- **Database Testing**: Utilities for PostgreSQL and IBM DB2
- **Logging**: Timestamped logs for every run
- **Allure Reporting**: Rich, step-based reporting for UI and API
- **Parallel Execution**: Out-of-the-box support via pytest-xdist
- **Screenshots**: Automatic capture on test failure
- **Configurable**: All environment, browser, and DB settings via `config/config.yaml`

## Project Structure
```
├── apis/                # API test modules
├── config/              # YAML config files
├── db/                  # Database utility modules
├── files/               # Test data files
├── locators/            # Page locators
├── logs/                # Execution logs
├── pages/               # Page Object Model classes
├── reports/             # HTML and Allure reports
├── resourses/           # Test data (CSV, JSON)
├── screenshot/          # Screenshots on failure
├── tests/               # Test cases
├── utils/               # Utility classes (web, api, db, logger, etc.)
├── conftest.py          # Pytest fixtures and hooks
├── pytest.ini           # Pytest configuration
├── requirement.txt      # Python dependencies
├── docker-compose.yml   # (Optional) Selenium Grid setup
```

## Getting Started

### 1. Install dependencies
```bash
pip install -r requirement.txt
```

### 2. Configure your environment
Edit `config/config.yaml` to set browser, environment URLs, DB connection strings, and headless/grid options.

### 3. Run tests
- **UI Tests**:
  ```bash
  pytest tests/ --browser=chrome --environment=dev --headless
  ```
- **API Tests**:
  ```bash
  pytest -m api
  ```
- **Parallel Execution**:
  ```bash
  pytest -n 4
  ```
- **Generate HTML Report**:
  ```bash
  pytest --html=reports/report.html --self-contained-html
  ```

### 4. View Reports
- HTML: `reports/report.html`
- Allure: `allure serve reports/allure/allure-results`

## Customization
- Add new page classes in `pages/` and extend `BasePage`
- Add new API utilities in `utils/api_utility.py`
- Add new DB utilities in `utils/database_utility.py`

## Best Practices
- Use markers (`@pytest.mark.smoke`, `@pytest.mark.regression`, etc.) for test selection
- Use fixtures for setup/teardown
- Use the logger for all debug/info/error messages
- Keep test data in `resourses/`

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](LICENSE)




