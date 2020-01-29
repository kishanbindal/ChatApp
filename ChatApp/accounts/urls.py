from django.urls import path
from . import views


urlpatterns = [
    path('api/register/', views.UserRegistrationView.as_view(), name='registration-page'),
]