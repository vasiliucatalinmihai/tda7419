import json
import os.path


class Storage:

    AUTOLOAD_MODULES = 0
    AUTOSAVE = 1

    _path_to_files = '~/tda7419/_storage/'
    _general_config = 'general_config'

    _data = dict()
    _module_file = dict()
    _module_loaded = dict()

    # * main constructor
    def __init__(self):
        self.init(self._general_config)

    def init(self, module):
        self._module_file[module] = self._path_to_files + module + '.json'

        if not os.path.exists(self._get_file_name(module)):
            open(self._get_file_name(module), "w").close()
            self._data[module] = dict()
            self._save(module)

        if self.AUTOLOAD_MODULES:
            self._load_module(module)
            self._module_loaded[module] = True

        return self

    def get_config(self, key=False):
        return self.get_data(self._general_config, key)

    def get_data(self, module, key=False):

        if module not in self._module_loaded or not self._module_loaded[module]:
            self._load_module(module)
            self._module_loaded[module] = True

        if not key:
            return self._data[module]

        value = False

        if key in self._data[module].keys():
            value = self._data[module][key]

        return value

    def set_data(self, module, key, value):
        if not self._module_loaded[module]:
            self._load_module(module)
            self._module_loaded[module] = True

        self._data[module][key] = value

        if self.AUTOSAVE:
            self._save(module)

        return self

    def set_all_data(self, module, data):
        self._data[module] = data

        if self.AUTOSAVE:
            self._save(module)

        return self

    def _load_module(self, module):
        self._data[module] = json.loads(self._read_file(self._get_file_name(module)))

    @staticmethod
    def _read_file(file_path):
        resource = open(file_path, 'r')

        try:
            content = resource.read()
            resource.close()
        finally:
            resource.close()

        return content

    def _get_file_name(self, module):
        if module not in self._module_file.keys():
            raise Exception('Uninitialized module ' + module)

        return self._module_file[module]

    def _save(self, module):
        file = self._get_file_name(module)

        with open(file, 'w') as outfile:
            json.dump(self._data[module], outfile)

        return self
