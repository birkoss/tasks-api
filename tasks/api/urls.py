from django.urls import path

from . import views as api_views


urlpatterns = [
    path('api/tasks/<str:group_pk>', api_views.tasksList.as_view(), name='tasks'),
    path('api/task/<str:pk>', api_views.TaskDetail.as_view(), name='task'),
]
