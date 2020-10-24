from scratch:
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
 python -m pytest --alluredir=/tmp/my_allure_results tests/test_google.py
9. view allure results: 
allure serve /tmp/my_allure_results
