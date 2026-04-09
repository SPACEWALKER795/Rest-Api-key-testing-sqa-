# SQA REST API Test Suite

An automated Software Quality Assurance framework built in Python that tests the [JSONPlaceholder](https://jsonplaceholder.typicode.com) REST API. The project implements 6 types of testing across 23 test cases, generates 3 different reports, and runs automatically via a GitHub Actions CI/CD pipeline.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Running the Tests](#running-the-tests)
- [Test Types](#test-types)
- [Reports](#reports)
- [CI/CD Pipeline](#cicd-pipeline)
- [Enhancements](#enhancements)

---

## Project Overview

Instead of manually testing an API every time code changes, this project automates the entire process. Python scripts send real HTTP requests to the API, check the responses against expected values, and generate detailed visual reports — all in under 20 seconds.

**What is tested:** The JSONPlaceholder API, a free public REST API that provides fake data for users, posts, comments, todos, and albums.

**Key results:**
- 23 test cases — 100% pass rate
- 6 test suites covering all major SQA techniques
- 3 report types generated automatically
- Full CI/CD pipeline via GitHub Actions

---

## Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11 | Core language |
| pytest | latest | Test runner — finds and executes all tests |
| requests | latest | Sends HTTP GET, POST, DELETE calls to the API |
| coverage.py | latest | Measures which lines of code were tested |
| pytest-html | latest | Generates HTML test results report |
| allure-pytest | latest | Generates professional visual dashboard |
| pytest-mock | latest | Mocking support for offline tests |
| pytest-rerunfailures | latest | Retries flaky tests automatically |
| pytest-json-report | latest | Exports results to JSON for custom dashboard |
| GitHub Actions | — | Runs full test suite on every git push |

---

## Project Structure

```
sqa-project/
│
├── api_client.py              # Main code — all API call functions
├── pytest.ini                 # pytest config — markers and settings
├── allure.properties          # Allure config
├── categories.json            # Allure failure categories
├── generate_dashboard.py      # Script to generate custom HTML dashboard
├── run_tests.bat              # Windows batch file to run everything at once
├── results.json               # Auto-generated test results (JSON)
├── report.html                # Auto-generated pytest-html report
├── dashboard.html             # Auto-generated custom HTML dashboard
│
├── data/
│   └── test_data.json         # All test input data in one place
│
├── tests/
│   ├── conftest.py            # Shared fixtures used by all test files
│   ├── test_basic.py          # Smoke tests — basic API health checks
│   ├── test_users.py          # Parameterized tests — multiple user inputs
│   ├── test_schema.py         # Schema validation — field and type checks
│   ├── test_negative.py       # Negative tests — invalid and edge case inputs
│   ├── test_performance.py    # Performance tests — response time checks
│   ├── test_mocked.py         # Mocking tests — tests without real internet
│   ├── test_data_driven.py    # Data-driven tests — reads from test_data.json
│   └── test_extended.py       # Extended tests — comments, todos, albums
│
├── allure-results/            # Auto-generated Allure data folder
│   ├── environment.properties # Environment info shown on Allure dashboard
│   └── categories.json        # Failure categories config
│
├── htmlcov/                   # Auto-generated coverage report folder
│
└── .github/
    └── workflows/
        └── test.yml           # GitHub Actions CI/CD pipeline
```

---

## Installation & Setup

### Prerequisites

Make sure you have the following installed:

- [Python 3.11+](https://python.org/downloads) — tick "Add Python to PATH" during install
- [Java JDK 21+](https://oracle.com/java/technologies/downloads) — required for Allure
- [Git](https://git-scm.com)
- [Allure CLI](https://github.com/allure-framework/allure2/releases/latest) — download the `.zip`, extract to `C:\allure`, add `C:\allure\bin` to your system PATH

### Step 1 — Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/sqa-project.git
cd sqa-project
```

### Step 2 — Install all Python dependencies

```bash
pip install pytest requests coverage pytest-html allure-pytest pytest-mock pytest-rerunfailures pytest-json-report
```

### Step 3 — Verify everything is installed

```bash
py -m pytest --version
allure --version
java --version
```

All three should print version numbers. If `pytest` is not found, use `py -m pytest` instead throughout this guide.

---

## Running the Tests

### Quickest way — run everything at once (Windows)

```bash
.\run_tests.bat
```

This single command cleans old results, runs all tests twice (for Allure trend history), copies the categories file, writes environment info, generates the custom dashboard, and opens the Allure report automatically.

---

### Manual step-by-step commands

**Run all tests with HTML report and coverage:**

```bash
py -m coverage run -m pytest tests/ --html=report.html -v
py -m coverage html
```

**Run tests and generate Allure report:**

```bash
rmdir /s /q allure-results
py -m pytest tests/ --alluredir=allure-results -v
copy categories.json allure-results\categories.json
echo Base.URL=https://jsonplaceholder.typicode.com > allure-results\environment.properties
echo Project.Name=SQA REST API Test Suite >> allure-results\environment.properties
echo Environment=Test >> allure-results\environment.properties
echo Developer=Rehan >> allure-results\environment.properties
echo Python.Version=3.11 >> allure-results\environment.properties
allure serve allure-results
```

**Generate custom HTML dashboard:**

```bash
py -m pytest tests/ --json-report --json-report-file=results.json -v
py generate_dashboard.py
```

Then open `dashboard.html` in your browser.

**Run only specific test categories:**

```bash
py -m pytest tests/ -m smoke       # Quick sanity tests only
py -m pytest tests/ -m regression  # Full detailed tests only
py -m pytest tests/ -m negative    # Edge case tests only
```

---

## Test Types

### 1. Smoke Tests — `tests/test_basic.py` (4 tests)

Quick sanity checks to verify the API is alive and returning data.

```python
@pytest.mark.smoke
def test_get_user_success():
    response = get_user(1)
    assert response.status_code == 200
    assert response.json()["id"] == 1
```

### 2. Parameterized Tests — `tests/test_users.py` (8 tests)

One test function runs automatically for multiple inputs. 5 users tested with 1 function.

```python
@pytest.mark.parametrize("user_id", [1, 2, 3, 4, 5])
def test_multiple_users_exist(user_id):
    response = get_user(user_id)
    assert response.status_code == 200
```

### 3. Schema Validation — `tests/test_schema.py` (3 tests)

Checks every required field exists and has the correct data type.

```python
def test_user_required_fields(base_url, sample_user):
    data = requests.get(f"{base_url}/users/1").json()
    for field in ["id", "name", "username", "email", "address", "phone"]:
        assert field in data
```

### 4. Negative Tests — `tests/test_negative.py` (6 tests)

Tests invalid and boundary inputs to verify the API handles errors gracefully.

```python
@pytest.mark.parametrize("bad_id", [0, -1, -999])
def test_invalid_user_ids(bad_id):
    response = get_user(bad_id)
    assert response.status_code in [400, 404]
```

### 5. Performance Tests — `tests/test_performance.py` (2 tests)

Measures response time and fails the test if the API is too slow.

```python
def test_single_user_response_time():
    start = time.time()
    response = get_user(1)
    duration = time.time() - start
    assert duration < 3.0, f"Too slow: {duration:.2f}s"
```

### 6. Mocking Tests — `tests/test_mocked.py` (3 tests)

Fakes the API response using `unittest.mock` so tests run without real internet.

```python
def test_get_user_mocked():
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"id": 1, "name": "Fake User"}
    with patch("api_client.requests.get", return_value=mock_resp):
        response = get_user(1)
        assert response.status_code == 200
```

---

## Reports

### 1. Allure Dashboard (Primary)

The most detailed report with severity badges, step-by-step timelines, and failure categories.

```bash
allure serve allure-results
```

Opens automatically in your browser at `http://127.0.0.1:PORT`.

Features:
- Severity levels: CRITICAL, NORMAL, MINOR on every test
- Step-by-step clickable execution timeline per test
- Categories tab: classifies failures as broken, assertion error, timeout
- Environment panel: shows project name, URL, developer, Python version
- Trend graph: shows pass rate history across multiple runs

### 2. Custom HTML Dashboard

A Python-generated visual dashboard with charts.

```bash
py generate_dashboard.py
```

Open `dashboard.html` in your browser.

Features:
- Metric cards: total tests, passed, failed, pass rate, duration
- Donut chart: pass vs fail breakdown
- Bar chart: tests by category (smoke / regression / negative)
- Horizontal bar chart: per-test duration (green = pass, red = fail)
- Response time chart: actual time vs 3-second limit
- Interactive filter bar: filter table by result or category
- Test run history table

### 3. Coverage Report

Shows which lines of your code were executed during tests.

```bash
py -m coverage html
```

Open `htmlcov/index.html` in your browser. Lines highlighted in red were not tested. Target: 80%+ coverage.

### 4. pytest-html Report

Simple pass/fail report generated alongside every test run.

Open `report.html` in your browser after running tests.

---

## CI/CD Pipeline

Every time you push code to GitHub, the full test suite runs automatically via GitHub Actions.

**File:** `.github/workflows/test.yml`

```yaml
name: SQA Test Suite
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install pytest requests coverage pytest-html allure-pytest pytest-mock pytest-rerunfailures pytest-json-report
      - name: Run all tests
        run: coverage run -m pytest tests/ --html=report.html -v
      - name: Coverage report
        run: coverage html
```

After pushing, go to your GitHub repository → Actions tab → see the green checkmark (all pass) or red X (something failed).

---

## Enhancements

The project includes several advanced SQA features beyond the basics:

**Data-driven testing** — `tests/test_data_driven.py` reads all test inputs from `data/test_data.json`. To add more test cases, edit the JSON file — no Python code changes needed.

**Allure decorators** — every test has `@allure.title`, `@allure.description`, `@allure.severity`, and `allure.step()` blocks for a fully detailed report.

**Test markers** — tests are organised into `smoke`, `regression`, and `negative` categories and can be run independently.

**Retry on failure** — `pytest-rerunfailures` retries flaky tests up to 3 times before marking them as failed, handling temporary network issues.

**Extended endpoint coverage** — `tests/test_extended.py` covers the comments, todos, and albums endpoints in addition to users and posts.

---

## API Reference

All tests run against the [JSONPlaceholder API](https://jsonplaceholder.typicode.com) — a free public REST API.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/users` | GET | Get all users |
| `/users/{id}` | GET | Get user by ID |
| `/posts` | GET | Get all posts |
| `/posts` | POST | Create a new post |
| `/posts/{id}` | DELETE | Delete a post |
| `/posts/{id}/comments` | GET | Get comments for a post |
| `/users/{id}/todos` | GET | Get todos for a user |
| `/users/{id}/albums` | GET | Get albums for a user |

---

## Author

**Rehan** — SQA Project 2026

Built as part of a Software Quality Assurance course assignment demonstrating automated API testing with Python.
