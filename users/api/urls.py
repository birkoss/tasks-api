from django.urls import path

from . import views as api_views


urlpatterns = [
    path('api/register', api_views.userRegister.as_view(), name='register'),
    path('api/login', api_views.userLogin.as_view(), name='login'),
    path('api/getData', api_views.userData.as_view(), name='data'),

    path('api/user/task/<str:pk>',
         api_views.userTask.as_view(), name='user-task'),
    path('api/user/tasks', api_views.userTasks.as_view(), name='user-tasks'),

    path('api/users/<str:group_pk>', api_views.userUsers.as_view(), name='users'),
]
