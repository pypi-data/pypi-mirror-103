from cloudtoken.core import utils


def handler(config: dict):
    password = utils.get_config_value(config, ["password"])
    return password
