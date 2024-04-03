from django.db import models

class APIConnection(models.Model):
    name = models.CharField(max_length=100, unique=True)
    base_url = models.URLField(max_length=200)
    auth_url = models.URLField(max_length=200, verbose_name="Authentication URL")
    endpoint = models.CharField(max_length=200, blank=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    token = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
