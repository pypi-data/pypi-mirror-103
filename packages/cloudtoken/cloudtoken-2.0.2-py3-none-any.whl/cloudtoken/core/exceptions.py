class CloudtokenException(Exception):
    pass


class AuthenticationError(CloudtokenException):
    pass


class ConfigurationFileError(CloudtokenException):
    pass


class ConfigurationError(CloudtokenException):
    pass


class PluginNotFoundError(CloudtokenException):
    pass


class PluginError(CloudtokenException):
    pass


class NoRolesFoundError(CloudtokenException):
    pass


class InvalidRoleIndex(CloudtokenException):
    pass


class ExportCredentials(CloudtokenException):
    def __init__(self, access_key, secret_key, token):
        super().__init__()
        self.access_key = access_key
        self.secret_key = secret_key
        self.token = token


class CloudtokenKeyringError(CloudtokenException):
    pass
