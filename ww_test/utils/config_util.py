import yaml
from utils.file_util import FileUtil


class ConfigUtil(object):


    def __init__(self):
        self.config = None

    def read_yaml(self, filename):
        filename = FileUtil.get_full_path(filename)
        with open(filename, 'r', encoding='utf8') as file:
            self.config = yaml.safe_load(file)
            return self.config

    def get_yaml(self, key, section_name='root'):
        if self.config and section_name in self.config and key in self.config[section_name]:
            return self.config[section_name][key]
        return None
    
    def get_yaml_value(self, filename,section_name,key):
        config = self.read_yaml(filename)
        if config and section_name in config and key in config[section_name]:
            yaml_info = config[section_name]
            value = yaml_info[key]
            return value
        return None
        

