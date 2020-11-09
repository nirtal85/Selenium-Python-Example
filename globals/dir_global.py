import os

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
INI_CONFIGS_PATH = os.path.join(ROOT_DIR, "ini_configs")
DATA_FILES_PATH = os.path.join(ROOT_DIR, "data")
ENV_FILE_PATH = os.path.join(ROOT_DIR, "allure-results")
# Creating allure-results directory
if not os.path.exists(ENV_FILE_PATH):
    os.mkdir(ENV_FILE_PATH)
