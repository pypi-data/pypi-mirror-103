import json
import os


class FipibarConfig():

    def __init__(self):
        '''
        TODO:
        '''
        self.path = os.path.expanduser("~") + "/.fipibar_config.json"
        pass

    def get(self, key, default):
        if not os.path.exists(self.path):
            return default
        try:
            with open(self.path, 'r') as fh:
                config = json.load(fh)

                if key in config.keys():
                    return config[key]
                else:
                    return default
        except Exception as e:
            print("Problem reading from ~/.fipibar_config.json!")
            print(e)

    def set(self, key, value):
        config = None

        try:
            with open(self.path, 'r') as fh:
                config = json.load(fh)
        except Exception as e:
            print("Problem reading from ~/.fipibar_config.json!")
            print(e)

            return

        config[key] = value

        try:
            with open(self.path, 'w') as fh:
                json.dump(config, fh)
        except Exception as e:
            print("Problem writing to ~/.fipibar_config.json!")
            print(e)

            return
