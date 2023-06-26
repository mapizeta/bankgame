from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("base.urls",namespace="base")),
    path('admin/', admin.site.urls),
]
