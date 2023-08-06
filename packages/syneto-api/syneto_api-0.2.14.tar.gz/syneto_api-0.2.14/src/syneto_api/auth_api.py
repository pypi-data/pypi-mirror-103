import os
from .api_client import APIClientBase


class Authentication(APIClientBase):
    def __init__(self, url_base=None, **kwargs):
        super().__init__(url_base or os.environ.get("AUTH_SERVICE", ""), **kwargs)

    def login(self, username: str, password: str):
        body = {"username": username, "password": password}
        return self.post_request("/login", body=body)

    def get_public_key(self, username: str):
        return self.post_request("/public-key", query_args={"username": username})

    def add_authorized_key(self, username: str, public_key: str):
        return self.post_request(
            "/authorized-keys",
            query_args={"username": username},
            body={"public_key": public_key},
        )

