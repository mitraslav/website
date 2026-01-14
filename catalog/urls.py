from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),                # корень сайта: /
    path('contacts/', views.contacts, name='contacts'),  # /contacts/
]
