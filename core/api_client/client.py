import requests
from django.core.exceptions import ImproperlyConfigured
from .models import APIConnection

class ClientAPI:
    def __init__(self, api_name):
        try:
            self.api = APIConnection.objects.get(name=api_name, active=True)
        except APIConnection.DoesNotExist:
            raise ValueError(f"API connection settings named '{api_name}' not found or not active.")
        
        self.base_url = self.api.base_url
        self.headers = {'Content-Type': 'application/json'}

        if self.api.token:
            self.headers['Authorization'] = f"Token {self.api.token}"
        else:
            self.authenticate()

    def authenticate(self):
        if self.api.username and self.api.password:
            try:
                response = requests.post(self.api.auth_url, data={"username": self.api.username, "password": self.api.password})
                response.raise_for_status()
                self.api.token = response.json().get('token')
                if not self.api.token:
                    raise ImproperlyConfigured(f"No token received from API '{self.api.name}' during authentication.")
                self.headers['Authorization'] = f"Token {self.api.token}"
                self.api.save()
            except requests.RequestException as e:
                raise ImproperlyConfigured(f"Failed to authenticate with API '{self.api.name}': {e}")
        elif not self.api.token:
            raise ValueError("Authentication requires username/password or an existing token.")

    def request(self, method, endpoint, data=None):
        url = f'{self.base_url}/{endpoint}'.rstrip("/")
        response = requests.request(method=method, url=url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
