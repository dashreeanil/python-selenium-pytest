#!/bin/bash
echo "Running Selenium test suite in headless QA mode..."
pytest --environment=qa --headless -v --tb=short