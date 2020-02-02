from django.urls import path
from . import views


urlpatterns = [
    path('api/register/', views.UserRegistrationView.as_view(), name='registration-page'),
    path('activate/<token>', views.activate, name='account-activation'),
    path('api/login/', views.UserLoginView.as_view(), name='login-page'),
    path('api/logout/', views.UserLogOutView.as_view(), name='logout'),
    path('api/forgotpassword', views.UserForgotPasswordView.as_view(), name='forgot-password'),
    path('reset/<token>', views.reset, name='reset-password'),

]