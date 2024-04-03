from django.urls import path
from .views import manage_api_connections, edit_api_connection

urlpatterns = [
    path('connections/', manage_api_connections, name='manage_api_connections'),
    path('connections/edit/<int:pk>/', edit_api_connection, name='edit_api_connection'),
]
