


🧪 Selenium Grid Test Automation (Dockerized)
This framework enables parallel browser testing using Selenium Grid, Docker, and Pytest. It supports dynamic environment selection, headless mode, and test markers.

📦 Prerequisites
- Python 3.8+
- Docker & Docker Compose
- Install dependencies:
pip install -r requirements.txt



🚀 Run Tests with Dockerized Grid
Use the run_tests.py runner to start the Grid, wait for readiness, and execute tests in parallel.
python run_tests.py [options]


✅ Available Options
| Flag | Description | Example | 
| --env | Target environment (dev, qa, staging, prod) | --env=qa | 
| --browser | Browser to use (chrome, firefox) | --browser=firefox | 
| --headless | Run browser in headless mode | --headless | 
| --markers | Run tests with specific pytest markers | --markers=smoke | 
| --workers | Number of parallel pytest workers | --workers=6 | 



🧱 Docker Grid Setup
The Grid is defined in docker-compose.yml with:
- 1 Selenium Hub
- 2 Chrome Nodes
- 2 Firefox Nodes
To start manually:
docker-compose up -d


To stop:
docker-compose down



📁 Project Structure
├── config/
│   └── config.yaml         # Environment and browser settings
├── tests/                  # Your test suite
├── conftest.py             # Pytest fixtures and Grid integration
├── run_tests.py            # Test runner with Docker orchestration
├── docker-compose.yml      # Selenium Grid setup
└── screenshot/             # Failure screenshots




