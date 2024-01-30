# Selenium Python Example

![twitter](https://img.shields.io/twitter/follow/NirTal2)
![dev run](https://github.com/nirtal85/Selenium-Python-Example/actions/workflows/devRun.yml/badge.svg)
![nightly](https://github.com/nirtal85/Selenium-Python-Example/actions/workflows/nightly.yml/badge.svg)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Tech Stack

| Tool                                                                             | Description                                                             |
|----------------------------------------------------------------------------------|-------------------------------------------------------------------------|
| [selenium](https://pypi.org/project/selenium/)                                   | A powerful tool for automating web browsers and conducting web tests    |
| [pytest](https://pypi.org/project/pytest/)                                       | A popular testing framework for Python                                  |
| [pytest-base-url](https://pypi.org/project/pytest-base-url/)                     | Pytest plugin for setting a base URL for your tests                     |
| [python-dotenv](https://pypi.org/project/python-dotenv/)                         | Loads environment variables from a .env file, simplifying configuration |
| [mailinator-python-client](https://pypi.org/project/mailinator-python-client-2/) | A Python client for interacting with the Mailinator email service       |
| [visual-regression-tracker](https://pypi.org/project/visual-regression-tracker/) | Performs visual regression testing                                      |
| [pytest-check](https://pypi.org/project/pytest-check/)                           | Provides additional checking functionality for your Pytest tests        |
| [pytest-rerunfailures](https://pypi.org/project/pytest-rerunfailures/)           | Pytest plugin to rerun failed tests automatically                       |
| [allure-pytest](https://pypi.org/project/allure-pytest/)                         | Integrates Allure reporting with your Pytest tests for better reporting |
| [requests](https://pypi.org/project/requests/)                                   | A versatile library for making HTTP requests in Python                  |
| [tenacity](https://pypi.org/project/tenacity/)                                   | Retrying library                                                        |
| [pytest-dependency](https://pypi.org/project/pytest-dependency/)                 | Pytest plugin that allows declaring dependencies between tests          |
| [Deprecated](https://pypi.org/project/Deprecated/)                               | A library for emitting warnings about deprecated code                   |
| [dataclasses-json](https://pypi.org/project/dataclasses-json/)                   | A library for serialization of dataclasses to and from JSON             |
| [mysql-connector-python](https://pypi.org/project/mysql-connector-python/)       | Interface for connecting to MySQL databases and executing SQL queries   |

## Articles Written About This Project

* [Test Automation - How To Build a CI/CD Pipeline Using Pytest and GitHub Actions](https://www.linkedin.com/pulse/test-automation-how-build-cicd-pipeline-using-pytest-nir-tal/)
* [Test Automation - How To Attach Public IP Address to Allure report using Pytest and Requests](https://www.linkedin.com/pulse/test-automation-how-attach-public-ip-adress-allure-report-nir-tal/)
* [Test Automation - Selenium Example Python Project 2022 Updates](https://www.linkedin.com/pulse/test-automation-selenium-example-python-project-2022-nir-tal/)
* [Test Automation - How To Add Git Version Control Data To Allure Report in Python](https://www.linkedin.com/pulse/test-automation-how-add-git-version-control-data-allure-nir-tal/)
* [Test Automation - How To Attach Session Storage, Local Storage, Cookies, and Console logs To Allure Report in Selenium Python](https://www.linkedin.com/pulse/test-automation-how-attach-session-storage-local-cookies-nir-tal/)
* [Test Automation - How To Capture Full-Page Screenshots In Selenium Python Using Chrome DevTools Protocol](https://www.linkedin.com/pulse/test-automation-how-capture-full-page-screenshots-selenium-nir-tal/)
* [Test Automation - How To Edit Cookies in Selenium Python](https://www.linkedin.com/pulse/test-automation-how-edit-cookies-selenium-python-nir-tal/)
* [Test Automation - Pre-Merge Testing with GitHub Actions: A Step-by-Step Guide](https://www.linkedin.com/pulse/test-automation-pre-merge-testing-github-actions-step-by-step-tal/)

## Setup Instructions

### Step 1: Clone the project

```bash
git clone https://github.com/nirtal85/Selenium-Python-Example.git
cd selenium-python-example
```

### Step 2: Create and activate a virtual environment

#### For Windows:
```bash
py -m pip install --user virtualenv
py -m venv env
.\env\Scripts\activate
```

#### For Mac:
```bash
python3 -m pip install --user virtualenv
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Poetry

```bash
pip install poetry
```

### Step 4: Install Project Dependencies

```bash
poetry install --no-root
```

### Step 5: Create .env File

Create a `.env` file in the project root directory to securely store project secrets and configuration variables. This
file will be used to define key-value pairs for various parameters required by the project. Add the following properties
to the `.env` file:

| Parameter              | Description                             | Example Value                 |
|------------------------|-----------------------------------------|-------------------------------|
| EMAIL                  | Your email address for authentication   | "your@email.com"              |
| PASSWORD               | Your secret password for authentication | "your_secret_password"        |
| VRT_APIURL             | Visual Regression Tracker API URL       | "https://vrt.example.com/api" |
| VRT_PROJECT            | Visual Regression Tracker Project ID    | "project_id"                  |
| VRT_CIBUILDID          | Visual Regression Tracker Build Number  | "build_number"                |
| VRT_BRANCHNAME         | Visual Regression Tracker Branch Name   | "main"                        |
| VRT_APIKEY             | Visual Regression Tracker API Key       | "your_api_key"                |
| VRT_ENABLESOFTASSERT   | Enable Soft Assertions                  | True (or False)               |
| MAILINATOR_API_KEY     | API Key for Mailinator service          | "your_mailinator_api_key"     |
| MAILINATOR_DOMAIN_NAME | Domain name for Mailinator              | "your_mailinator_domain"      |

## Running Tests

```bash
pytest --browser <firefox/chrome_headless>
```

When no browser was selected then chrome will be used.

* Run according to tags:

```bash
pytest -m <tag_name> --browser <firefox/chrome_headless>
```

## Viewing Test Results

### Install Allure Commandline To View Test results

#### For Windows:

Follow the instructions [here](https://scoop.sh/) to install Scoop.<br>
Run the following command to install Allure using Scoop:

```bash
scoop install allure
```

#### For Mac:

```bash
brew install allure
```

### View Results Locally:

```bash
allure serve allure-results
```

### View Results Online:

[View allure results via Github pages](https://nirtal85.github.io/Selenium-Python-Example/)

## View Help And Other CLI Options

```bash
pytest --help
```

### Pre Commit

#### Run Pre Commit Checks Automatically

```bash
pre-commit install
```

#### Bump Pre Commit Hooks Version

```bash
pre-commit autoupdate
```

#### Run Pre Commit Checks Manually On The Entire Project

```bash
pre-commit run --all-files
```
