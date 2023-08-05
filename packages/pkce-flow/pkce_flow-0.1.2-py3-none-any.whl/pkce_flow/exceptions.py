class BasePKCEFlowError(Exception):
    pass


class PKCEFlowError(BasePKCEFlowError):
    def __init__(self, response=None):
        self.response = response


class ImproperlyConfigured(BasePKCEFlowError):
    pass


class StateForgeryError(BasePKCEFlowError):
    pass
