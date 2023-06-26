from django.urls import path
from .views import *

app_name = 'base'

urlpatterns = [
    path("", Index.as_view(), name='index'),
    path("home/", Home.as_view(), name="home"),
    path("transaction", TransactionRedirectView.as_view(), name='transaction'),
]