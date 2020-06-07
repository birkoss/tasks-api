from django.urls import path

from . import views as api_views


urlpatterns = [
    path('api/register', api_views.userRegister.as_view(), name='register'),
    path('api/login', api_views.userLogin.as_view(), name='login'),
    path('api/getData', api_views.userData.as_view(), name='data'),
    path('api/users/<str:group_pk>', api_views.userUsers.as_view(), name='users'),
]
