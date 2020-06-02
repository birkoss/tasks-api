from django.urls import path

from . import views as api_views


urlpatterns = [
    path('api/register', api_views.userRegister.as_view(), name='register'),
    path('api/login', api_views.userLogin.as_view(), name='login'),
]
