import configparser
import os

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