# QA Automation Tests for Room Booking Application

## Project Overview

This project is a comprehensive Test Automation Framework designed 
to verify the functionality of the [Restful Booker Platform](https://automationintesting.online). 
It covers both **API** and **UI** testing layers to ensure the stability of the room booking system.

---
The framework supports:
* **API Testing**: Admin operations (CRUD for rooms), booking management, 
and data validation using `requests`.
* **UI Testing**: User interactions, booking forms, calendar validations, 
and responsive checks using `playwright`.
---

## Tech Stack

* **Language**: Python
* **Test Runner**: Pytest
* **UI Automation**: Playwright
* **API Automation**: Requests
* **Logging**: Loguru
* **Parallel Execution**: pytest-xdist

---

## Project Structure

```text
├── page_object/        # Page Object Model (POM) classes
│   └── base_page.py    # UI Selectors of common elements
│   └── booking_page.py # UI Selectors and methods for Booking Page
│   └── home-page.py    # UI Selectors and methods for Home Page
├── tests/              # Test scripts
│   ├── conftest.py     # Pytest fixtures and hooks
│   ├── test_admin_api.py # API tests for Admin functionality
│   └── test_user_ui.py   # UI tests for User functionality
├── utils/              # Utility helper classes
│   ├── test_data.py    # Test data constants
│   ├── utils_api.py    # API wrapper methods
│   └── constants_ui.py # Constants for UI tests
├── test_data.json      # Externalized test data
├── .flake8             # Flake8 configuration for code style
├── .gitignore          # Git ignore file
├── README.md           # Project documentation
├── pytest.ini          # Pytest configuration and markers
└── requirements.txt    # Project dependencies
```
---

### Hou to start
1. Clone the repository:
  ```Bash
    git clone <repository-url>
    cd <repository-directory>
  ```

2. Create and activate a virtual environment:

 ```Bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
  ```

3. Install dependencies:

```Bash
  pip install -r requirements.txt
```

4. Install Playwright browsers (required for UI tests to run).
```Bash
  playwright install
```

5. Run tests:
  ```Bash
    pytest
  ```

6. Start only UI tests:
  ```Bash
  pytest -m ui -n auto
  ```
7. Run specific UI scenarios
```bash
    pytest -m ui_test_1  # Valid Booking
    pytest -m ui_test_2  # Invalid Booking
    pytest -m ui_test_3  # Unavailable Dates Check
    pytest -m ui_test_4  # Page Load Check
  ```
8. For disable headless mode, change the parameter in the tests to `headless=False`.
9. Start only API tests:
  ```bash
  pytest -m api
  ```
10. Test data can be modified in the [`test_data.json`](./test_data.json) file for different scenarios.

---
## Test Cases
- A human-readable list of test scenarios covered by this framework
can be found in the test-cases.txt file.
---

## Logging and Reports
- The project uses Loguru for logging.
- Console Output: Brief info about test execution.
- File Logs: Detailed debug logs are saved to test_result_{date}.log.
- Test Reports: Pytest generates HTML reports for test results into test_report.html file.

