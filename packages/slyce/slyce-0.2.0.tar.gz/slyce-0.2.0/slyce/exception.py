class SlyceError(Exception):
    pass


class InvalidCredentials(SlyceError):
    def __init__(self):
        super().__init__('Missing or invalid credentials.')


class ExecuteWorkflowError(SlyceError):
    pass


class UploadImageError(SlyceError):
    pass
