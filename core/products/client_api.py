import requests

class ClientAPI:
    def __init__(self, base_url, endpoint, username=None, password=None, token=None):
        self.base_url = base_url
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.token = token

    def authenticate(self):
        if self.username and self.password:
            response = requests.post(f"{self.base_url}/auth/", data={"username": self.username, "password": self.password})
            response.raise_for_status()
            self.token = response.json()['token']
        elif not self.token:
            raise ValueError("Authentication requires username/password or an existing token")

    def test_connection(self):
        self.authenticate()
        response = requests.get(f"{self.base_url}/{self.endpoint}", headers={"Authorization": f"Token {self.token}"})
        response.raise_for_status()
        return True

    def _request(self, method, endpoint_suffix="", data=None):
        url = f"{self.base_url}/{self.endpoint}/{endpoint_suffix}".rstrip("/")
        headers = {"Authorization": f"Token {self.token}", "Content-Type": "application/json"}
        response = requests.request(method=method, url=url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def get(self, endpoint_suffix=""):
        return self._request('GET', endpoint_suffix)

    def post(self, data, endpoint_suffix=""):
        return self._request('POST', endpoint_suffix, data)

    def put(self, data, endpoint_suffix):
        if not endpoint_suffix:
            raise ValueError("PUT request requires an endpoint suffix.")
        return self._request('PUT', endpoint_suffix, data)

    def patch(self, data, endpoint_suffix):
        if not endpoint_suffix:
            raise ValueError("PATCH request requires an endpoint suffix.")
        return self._request('PATCH', endpoint_suffix, data)

    def delete(self, endpoint_suffix):
        if not endpoint_suffix:
            raise ValueError("DELETE request requires an endpoint suffix.")
        return self._request('DELETE', endpoint_suffix)