from django import forms
from .models import APIConnection

class APIConnectionForm(forms.ModelForm):
    class Meta:
        model = APIConnection
        fields = ['name', 'base_url', 'auth_url', 'endpoint', 'username', 'password', 'active']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
