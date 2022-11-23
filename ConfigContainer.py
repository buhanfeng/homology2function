import yaml
from yaml.loader import SafeLoader


class ConfigContainer:

    def __init__(self, p):
        with open(p, "r") as stream:
            try:
                self.globalConfig = yaml.load(stream, Loader=SafeLoader)
            except yaml.YAMLError as exc:
                print(exc)

    # ******************* feature field *****************
    globalConfig = None
