from slyce.client.admin import SlyceAdminClient as _SlyceAdminClient
from slyce.client.account import SlyceAccountClient as _SlyceAccountClient
from slyce.credentials import SlyceCredentials as _SlyceCredentials

from slyce.exception import InvalidCredentials


class SlyceClient:
    def __new__(cls, credentials: str = None, **kwargs):
        if not isinstance(credentials, _SlyceCredentials):
            try:
                if not credentials:
                    credentials = _SlyceCredentials.from_env()
                elif isinstance(credentials, dict):
                    credentials = _SlyceCredentials(**credentials)
            except Exception:
                raise InvalidCredentials

        if credentials.is_admin:
            return _SlyceAdminClient(credentials, **kwargs)

        return _SlyceAccountClient(credentials, **kwargs)
