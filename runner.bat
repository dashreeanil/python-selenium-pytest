@echo off
echo Running Selenium test suite in headless QA mode...

:: Run tests with both HTML and Allure reporting enabled
pytest --environment=qa --headless -v --tb=short ^
       --html=Reports/html_report.html ^
       --self-contained-html ^
       --alluredir=Reports/allure-results

echo Generating Allure report...
:: Optional: If you want to automatically open the Allure report after generation
allure generate Reports/allure-results --clean -o Reports/allure-report
:: allure open Reports/allure-report   <-- Uncomment this line if you want it to auto-launch

pause