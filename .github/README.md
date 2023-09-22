# Selenium Python Example

![dev run](https://github.com/nirtal85/Selenium-Python-Example/actions/workflows/devRun.yml/badge.svg)
![nightly](https://github.com/nirtal85/Selenium-Python-Example/actions/workflows/nightly.yml/badge.svg)

## Articles written about this project

* [Test Automation - How To Build a CI/CD Pipeline Using Pytest and GitHub Actions](https://www.linkedin.com/pulse/test-automation-how-build-cicd-pipeline-using-pytest-nir-tal/)
* [Test Automation - How To Attach Public IP Adress to Allure report using Pytest and Requests](https://www.linkedin.com/pulse/test-automation-how-attach-public-ip-adress-allure-report-nir-tal/)
* [Test Automation - Selenium Example Python Project 2022 Updates](https://www.linkedin.com/pulse/test-automation-selenium-example-python-project-2022-nir-tal/)
* [Test Automation - How To Add Git Version Control Data To Allure Report in Python](https://www.linkedin.com/pulse/test-automation-how-add-git-version-control-data-allure-nir-tal/)
* [Test Automation - How To Attach Session Storage, Local Storage, Cookies, and Console logs To Allure Report in Selenium Python](https://www.linkedin.com/pulse/test-automation-how-attach-session-storage-local-cookies-nir-tal/)
* [Test Automation - How To Capture Full-Page Screenshots In Selenium Python Using Chrome DevTools Protocol](https://www.linkedin.com/pulse/test-automation-how-capture-full-page-screenshots-selenium-nir-tal/)
* [Test Automation - How To Edit Cookies in Selenium Python](https://www.linkedin.com/pulse/test-automation-how-edit-cookies-selenium-python-nir-tal/)
* [Test Automation - Pre-Merge Testing with GitHub Actions: A Step-by-Step Guide](https://www.linkedin.com/pulse/test-automation-pre-merge-testing-github-actions-step-by-step-tal/)

## Project Setup

* [Install scoop](https://scoop.sh/)
* Install allure commandline by running the following command:

```bash
scoop install allure
```

* Clone the project
* Navigate to the project directory
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

* Install project dependencies:

```
poetry install
```

need to create .env file in the project root with the following properties:

| Parameter            | Description                             | Example Value                 |
|----------------------|-----------------------------------------|-------------------------------|
| EMAIL                | Your email address for authentication   | "your@email.com"              |
| PASSWORD             | Your secret password for authentication | "your_secret_password"        |
| VRT_APIURL           | Visual Regression Tracker API URL       | "https://vrt.example.com/api" |
| VRT_PROJECT          | Visual Regression Tracker Project ID    | "project_id"                  |
| VRT_CIBUILDID        | Visual Regression Tracker Build Number  | "build_number"                |
| VRT_BRANCHNAME       | Visual Regression Tracker Branch Name   | "main"                        |
| VRT_APIKEY           | Visual Regression Tracker API Key       | "your_api_key"                |
| VRT_ENABLESOFTASSERT | Enable Soft Assertions                  | True (or False)               |

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

* View allure results locally:

```bash
allure serve allure-results
```

* [View allure results via Github pages](https://nirtal85.github.io/Selenium-Python-Example/)

## View Help And Custom CLI Options

```bash
pytest --help
```

## Run pre commit checks automatically

```bash
pre-commit install
```

## Bump pre commit hooks version

```bash
pre-commit autoupdate
```


## Run pre commit checks manually on the entire project

```bash
pre-commit run --all-files
```

## Sort imports

```bash
isort .
```

## format code

```bash
black .
```
