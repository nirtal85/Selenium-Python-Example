![Python application](https://github.com/nirtal85/Selenium-Python-Example/workflows/Python%20application/badge.svg)

<u>Before all</u> <br>
* Install scoop from www.scoop.sh
* Install allure commandline by running the following command:
```
scoop install allure
```
<u>from scratch:</u> <br>

* git clone
* cd to project directory 
* Installing virtualenv:
```
py -m pip install --user virtualenv
```
* Creating a virtual environment: 
```
py -m venv env
```
* Activating a virtual environment:
```
.\env\Scripts\activate
```
* install pipenv enviorment:
```
pip install pipenv
```
7. 
```
pipenv install
```
* run tests:
```
pipenv run pytest --alluredir=allure-results --browser <firefox/remote/chrome_headless>
```
if no browser was selected then chrome will be used. 
* view allure results: 
```
allure serve allure-results
```

* Run according to tags:
```
pipenv run pytest -k "<tag_name>" --browser <firefox/chrome/remote/chrome_headless>
```

* GitHub Pages allure results:
https://github.com/nirtal85/Selenium-Python-Example/deployments/activity_log?environment=github-pages

* for help and custom CLI options:
```
pytest --help
```
