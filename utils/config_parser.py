import os

import configparser

from globals import dir_global


class ConfigParserIni:
    """ Parses ini files """

    def __init__(self, ini_file):
        self.config = configparser.ConfigParser()
        self.file_path = os.path.join(dir_global.INI_CONFIGS_PATH, ini_file)
        self.config.read(self.file_path)

    # returns ini file sections as dictionary
    def config_section_dict(self, section):
        section_dict = {}
        section_keys = self.config.options(section)
        for key in section_keys:
            try:
                section_dict[key] = self.config.get(section, key)
            except:
                print(f"exception found in {key}")
                section_dict[key] = None
        return section_dict


class AllureEnvironmentParser:
    """ Writes environment variables into allure environment file"""

    def __init__(self, file_name):
        self.file_path = os.path.join(dir_global.ALLURE_RESULTS_PATH, file_name)

    def write_to_allure_env(self, dic):
        with open(self.file_path, 'w+') as f:
            for key in dic:
                f.write(f'{key}={dic[key]}' + "\n")
