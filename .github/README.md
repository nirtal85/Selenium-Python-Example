# Selenium Python Example

![Python application](https://github.com/nirtal85/Selenium-Python-Example/workflows/Python%20application/badge.svg)

## Articles written about this project

1. [Test Automation - How To Build a CI/CD Pipeline Using Pytest and GitHub Actions](https://www.linkedin.com/pulse/test-automation-how-build-cicd-pipeline-using-pytest-nir-tal/)
2. [Test Automation - How To Attach Public IP Adress to Allure report using Pytest and Requests](https://www.linkedin.com/pulse/test-automation-how-attach-public-ip-adress-allure-report-nir-tal/)
3. [Test Automation - Selenium Example Python Project 2022 Updates](https://www.linkedin.com/pulse/test-automation-selenium-example-python-project-2022-nir-tal/)
4. [Test Automation - How To Add Git Version Control Data To Allure Report in Python](https://www.linkedin.com/pulse/test-automation-how-add-git-version-control-data-allure-nir-tal/)
5. [Test Automation - How To Attach Session Storage, Local Storage, Cookies, and Console logs To Allure Report in Selenium Python](https://www.linkedin.com/pulse/test-automation-how-attach-session-storage-local-cookies-nir-tal/)
6. [Test Automation - How To Capture Full-Page Screenshots In Selenium Python Using Chrome DevTools Protocol](https://www.linkedin.com/pulse/test-automation-how-capture-full-page-screenshots-selenium-nir-tal/)
7. [Test Automation - How To Edit Cookies in Selenium Python](https://www.linkedin.com/pulse/test-automation-how-edit-cookies-selenium-python-nir-tal/)

## Project Setup

* [Install scoop](https://scoop.sh/)
* Install allure commandline by running the following command:

```bash
scoop install allure
```

* clone the project
* navigate to the project directory
* Install virtualenv:

```bash
py -m pip install --user virtualenv
```

* Create a virtual environment:

```bash
py -m venv env
```

* Activate the virtual environment:

```bash
.\env\Scripts\activate
```

* Install pipenv:

```bash
pip install pipenv
```

* Install project dependencies using pipenv:

```
pipenv install
```

## Running Tests

```bash
pipenv run pytest --browser <firefox/chrome_headless>
```

When no browser was selected then chrome will be used.

* Run according to tags:

```bash
pipenv run pytest -m <tag_name> --browser <firefox/chrome_headless>
```

## Viewing Test Results

* View allure results locally:

```bash
allure serve allure-results
```

* [View allure results via Github pages](https://nirtal85.github.io/Selenium-Python-Example/)

## View Help And Custom CLI Options

```bash
pytest --help
```

## Sort imports

```bash
isort .
```

## format code

```bash
black .
```