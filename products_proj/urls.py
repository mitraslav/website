from django.urls import path
from products_proj.apps import ProductsProjConfig
from . import views

app_name = ProductsProjConfig.name

urlpatterns = [
    path('', views.index, name='home'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
]