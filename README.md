<u>Before all</u> <br>
1. Install scoop from www.scoop.sh
2. Install allure commandline by running the following command:
scoop install allure

<u>from scratch:</u> <br>

1. git clone
2. cd to project directory 
3. Installing virtualenv: 
py -m pip install --user virtualenv
4. Creating a virtual environment: 
py -m venv env
5. Activating a virtual environment:
.\env\Scripts\activate
6. pip install pipenv
7. pipenv install
8. run tests:
pipenv run pytest --alluredir=allure-results --browser <firefox/chrome/remote/chrome_headless> 
9. view allure results: 
allure serve allure-results

<u>Run according to tags:</u> <br>
1. pipenv run pytest -k "<tag_name>" --browser <firefox/chrome/remote/chrome_headless>

<u>GitHub Pages allure results:</u> <br>
https://nirtal85.github.io/selenium-python/<build_number>/