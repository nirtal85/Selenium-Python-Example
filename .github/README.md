![Python application](https://github.com/nirtal85/Selenium-Python-Example/workflows/Python%20application/badge.svg)

# Selenium Python Example

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

* install pipenv:

```
pip install pipenv
```

* install project dependencies using pipenv:

```
pipenv install
```

## Running Tests

```
pipenv run pytest --alluredir=allure-results --browser <firefox/chrome_headless>
```

if no browser was selected then chrome will be used.

* Run according to tags:

```
pipenv run pytest -k "<tag_name>" --browser <firefox/chrome_headless>
```

## Viewing Test Results

* view allure results:

```
allure serve allure-results
```

<ins>GitHub Pages allure results:</ins><br/>
https://github.com/nirtal85/Selenium-Python-Example/deployments/activity_log?environment=github-pages

## View Help And Custom CLI Options

```
pytest --help
```
