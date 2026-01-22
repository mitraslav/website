from django.urls import path
from . import views
from .views import ProductCreateView, ProductListView, ProductDetailView, ProductUpdateView, ProductDeleteView, ProductUnpublishView

app_name = 'catalog'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('home/', views.home, name='home'),                # корень сайта: /
    path('contacts/', views.contacts, name='contacts'),  # /contacts/
    path('add/', ProductCreateView.as_view(), name='product_add'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('<int:pk>/unpublish/', ProductUnpublishView.as_view(), name='product_unpublish')
]
