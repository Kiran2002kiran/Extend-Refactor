from django.urls import path
from .views import RegisterView
from rest_framework.permissions import AllowAny


urlpatterns=[
    path('api/register/',RegisterView.as_view(),name='register'),
]