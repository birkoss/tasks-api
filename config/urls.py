from django.contrib import admin
from django.urls import path

from users.api.urls import urlpatterns as users_urlpatterns
from tasks.api.urls import urlpatterns as tasks_urlpatterns

from tasks.views import test

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', test),
] + users_urlpatterns + tasks_urlpatterns
