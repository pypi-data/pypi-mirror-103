import requests
from .constants import base_url
from time import time
from .exceptions import ScopeError


class HTTPHandler:
    def __init__(self, auth):
        self.auth = auth

    def get_headers(self, **kwargs):
        headers = {
            'Authorization': f'Bearer {self.token}',
            **{key: value for key, value in kwargs.items() if value is not None}
        }
        return headers

    def __getattr__(self, method):
        if self.auth.expire_time <= time():
            self.auth.refresh_access_token()

        def func(self, path, data=None, **kwargs):
            if data is None:
                data = {}
            scope_required = path.scope
            if self.auth.scope < scope_required:
                raise ScopeError("You don't have the right scope to be able to do this.")
            headers = self.get_headers(**kwargs)
            response = getattr(requests, method)(base_url + path.path, headers=headers, data=data)
            response.raise_for_status()
            return response.json()
        return func
