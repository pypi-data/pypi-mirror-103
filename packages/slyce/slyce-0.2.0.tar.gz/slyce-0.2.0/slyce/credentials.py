import os
import json

from slyce.exception import InvalidCredentials

ENV_KEY = 'SLYCE_APPLICATION_CREDENTIALS'
SLYCE_ACCOUNT_ID = 'slyce'


class SlyceCredentials:
    @classmethod
    def from_env(cls):
        if ENV_KEY not in os.environ:
            raise ValueError(f"{ENV_KEY} not in environment variables.")
        return cls.from_file(os.environ[ENV_KEY])

    @classmethod
    def from_file(cls, filepath):
        with open(filepath, 'r') as f:
            credentials = json.load(f)
        return cls(**credentials)

    def __init__(self, api_key, account_id, space_id=None, **kwargs):
        if not api_key or not account_id or account_id != SLYCE_ACCOUNT_ID and not space_id:
            raise InvalidCredentials

        self._api_key = api_key
        self._account_id = account_id
        self._space_id = space_id

    @property
    def api_key(self):
        return self._api_key

    @property
    def account_id(self):
        return self._account_id

    @property
    def space_id(self):
        return self._space_id

    @property
    def is_admin(self):
        return self._account_id == SLYCE_ACCOUNT_ID
