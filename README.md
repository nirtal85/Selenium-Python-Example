<div align="center">

<img height="120" src="https://cdn.simpleicons.org/selenium/43B02A"/>

# Enterprise-Grade Selenium Python Architecture

### The Ultimate Boilerplate for Scalable, Robust, and Modern UI Automation

[![Twitter Follow](https://img.shields.io/twitter/follow/NirTal2?style=social)](https://twitter.com/NirTal2)
[![YouTube](https://img.shields.io/youtube/channel/subscribers/UCQjS-eoKl0a1nuP_dvpLsjQ?style=social)](https://www.youtube.com/channel/UCQjS-eoKl0a1nuP_dvpLsjQ)
![CI Status](https://github.com/nirtal85/Selenium-Python-Example/actions/workflows/devRun.yml/badge.svg)
![Nightly Build](https://github.com/nirtal85/Selenium-Python-Example/actions/workflows/nightly.yml/badge.svg)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

[View Live Report](https://nirtal85.github.io/Selenium-Python-Example/) • [Read The Docs](https://www.test-shift.com) • [Report Bug](https://github.com/nirtal85/Selenium-Python-Example/issues)

</div>

---

## 🚀 About The Project

This repository serves as a **Production-Ready Reference Architecture** for building high-scale automated testing frameworks using Python.

It demonstrates advanced design patterns, seamless CI/CD integration, and rich reporting capabilities that define modern Quality Engineering.

### ✨ Key Features

* **Modern Python Tooling:** Built with `uv` for lightning-fast dependency management and `Ruff` for linting.
* **Robust Reporting:** Full integration with **Allure Report**, including screenshots, logs, and video.
* **Visual Regression:** Integrated with **Visual Regression Tracker** for pixel-perfect UI validation.
* **CI/CD Ready:** Complete GitHub Actions workflows for Nightly runs, PR checks, and Report deployment.

---

## 📃 Articles written about this project

This project implements the concepts discussed in the following **TestShift** articles:

* [Test Automation - How To Build a CI/CD Pipeline Using Pytest and GitHub Actions](https://www.test-shift.com/posts/test-automation-how-to-build-a-ci-cd-pipeline-using-pytest-and-github-actions)
* [Test Automation - How To Attach Public IP Address to Allure report using Pytest and Requests](https://www.test-shift.com/posts/test-automation-how-to-attach-public-ip-adress-to-allure-report-using-pytest-and-requests)
* [Test Automation - Selenium Example Python Project 2022 Updates](https://www.test-shift.com/posts/test-automation-selenium-example-python-project-2022-updates)
* [Test Automation - How To Add Git Version Control Data To Allure Report in Python](https://www.test-shift.com/posts/test-automation-how-to-add-git-version-control-data-to-allure-report-in-python)
* [Test Automation - How To Attach Session Storage, Local Storage, Cookies, and Console logs To Allure Report in Selenium Python](https://www.test-shift.com/posts/test-automation-how-to-attach-session-storage-local-storage-cookies-and-console-logs-to-allure-report-in-selenium-python)
* [Test Automation - How To Capture Full-Page Screenshots In Selenium Python Using Chrome DevTools Protocol](https://www.test-shift.com/posts/test-automation-how-to-capture-full-page-screenshots-in-selenium-4-python-using-chrome-devtools-protocol)
* [Test Automation - How To Edit Cookies in Selenium Python](https://www.test-shift.com/posts/test-automation-how-to-edit-cookies-in-selenium-python)
* [Test Automation - Pre-Merge Testing with GitHub Actions: A Step-by-Step Guide](https://www.test-shift.com/posts/test-automation-pre-merge-testing-with-github-actions-a-step-by-step-guide)
* [Test Automation - How To Use Custom User Agent in Selenium Python or Playwright Python to Avoid Security Bots](https://www.test-shift.com/posts/test-automation-how-to-use-custom-user-agent-in-selenium-python-or-playwright-python-to-avoid-security-bots)
* [Test Automation - How to Use Dynamic Base URLs with Selenium And Playwright Python in GitHub Actions](https://www.test-shift.com/posts/test-automation-how-to-use-dynamic-base-urls-with-selenium-and-playwright-python-in-github-actions)
* [Test Automation Best Practices: Pinning Browser Version in Selenium Python for Stability](https://www.test-shift.com/posts/test-automation-best-practices-pinning-browser-version-in-selenium-python-for-stability/)
* [Test Automation - Capturing Console Logs and JavaScript Errors with Selenium WebDriver BiDi in Python](https://www.test-shift.com/posts/test-automation-capturing-console-logs-and-javascript-errors-with-selenium-webdriver-bidi-in-python)

---

## 🛠️ Tech Stack

| Tool                                                                             | Description & Why We Use It                                           |
|----------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| [Selenium](https://pypi.org/project/selenium/)                                   | The industry standard for browser automation.                         |
| [Pytest](https://pypi.org/project/pytest/)                                       | The most powerful and flexible testing framework for Python.          |
| [Allure](https://pypi.org/project/allure-pytest/)                                | For beautiful, data-rich test reports including screenshots and logs. |
| [Visual Regression Tracker](https://pypi.org/project/visual-regression-tracker/) | To catch UI bugs that functional tests miss (Pixel Perfect).          |
| [Assertpy](https://pypi.org/project/assertpy/)                                   | An expressive assertion library for readable tests.                   |
| [Dataclasses JSON](https://pypi.org/project/dataclasses-json/)                   | Easy serialization of objects for API/Data handling.                  |
| [MySQL Connector](https://pypi.org/project/mysql-connector-python/)              | Direct database validation.                                           |
| [Mailinator Client](https://pypi.org/project/mailinator-python-client-2/)        | For testing real email delivery workflows.                            |
| [Tenacity](https://pypi.org/project/tenacity/)                                   | Robust retrying mechanism for flaky network operations.               |

---

## ⚙️ Getting Started

### 1. Clone

```bash
git clone https://github.com/nirtal85/Selenium-Python-Example.git
cd selenium-python-example
```

### 2. Install (The Modern Way)

We use uv for lightning-fast installations.

Windows:

```bash
pip install uv
uv venv
.\env\Scripts\activate
uv sync --all-extras --dev
```

Mac/Linux:

```bash
pip install uv
uv venv
source .venv/bin/activate
uv sync --all-extras --dev
```

### 3. Configure

Create a .env file in the project root directory to securely store project secrets. This file is essential for authentication and environment configuration.

```properties
EMAIL="your@email.com"
PASSWORD="your_secret_password"
# ... add other variables as needed (see .env.example)
```

## 🏃‍♂️ Execution
Run all tests (Headless Chrome by default):

```bash
pytest
```

Run with specific browser:

```bash
pytest --driver firefox
```

Run specific suite (Tags):

```bash
pytest -m sanity
```

## 📊 Results & Reporting
We use Allure for reporting. To view results locally:

Windows (via Scoop):

```bash
scoop install allure
allure serve allure-results
```

Mac (via Brew):

```bash
brew install allure
allure serve allure-results
```

👉 [See a Live Example of the Report Here](https://nirtal85.github.io/Selenium-Python-Example/)

<div align="center">

Found this project useful?
If this architecture helped you solve a problem or save time, consider supporting the work!

<a href="https://www.buymeacoffee.com/nirtal"> <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" height="60" alt="Buy Me A Coffee" /> </a>

<br />

[Visit TestShift.com for more Architectural Insights](https://www.test-shift.com)

</div>