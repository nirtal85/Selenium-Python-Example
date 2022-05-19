# Selenium Python Example

![Python application](https://github.com/nirtal85/Selenium-Python-Example/workflows/Python%20application/badge.svg)

## Articles written about this project

1. [Test Automation - How To Build a CI/CD Pipeline Using Pytest and GitHub Actions
   ](https://www.linkedin.com/pulse/test-automation-how-build-cicd-pipeline-using-pytest-nir-tal/)
2. [Test Automation - How To Attach Public IP Adress to Allure report using Pytest and Requests
   ](https://www.linkedin.com/pulse/test-automation-how-attach-public-ip-adress-allure-report-nir-tal/)
3. [Test Automation - Selenium Example Python Project 2022 Updates
   ](https://www.linkedin.com/pulse/test-automation-selenium-example-python-project-2022-nir-tal/)

## Project Setup

* Install scoop from www.scoop.sh
* Install allure commandline by running the following command:

```
scoop install allure
```

* git clone
* cd to project directory
* Install virtualenv:

```
py -m pip install --user virtualenv
```

* Create a virtual environment:

```
py -m venv env
```

* Activate your virtual environment:

```
.\env\Scripts\activate
```

* Install pipenv:

```
pip install pipenv
```

* Install project dependencies using pipenv:

```
pipenv install
```

## Running Tests

```
pipenv run pytest --alluredir=allure-results --browser <firefox/chrome_headless>
```

When no browser was selected then chrome will be used.

* Run according to tags:

```
pipenv run pytest -m <tag_name> --browser <firefox/chrome_headless>
```

## Viewing Test Results

* View allure results locally:

```
allure serve allure-results
```

* View allure results via Github pages:<br/>
  https://nirtal85.github.io/Selenium-Python-Example/

## View Help And Custom CLI Options

```
pytest --help
```
