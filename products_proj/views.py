from django.shortcuts import render, get_object_or_404
from .models import Product

def home(request):
    latest = Product.objects.order_by('-created_at-')[:-5]

    print("Latest 5 products:", list(latest.values('id', 'name', 'created_at')))
    return render(request, 'home.html', {'latest': latest})

def index(request):
    """
    Главная: список продуктов.
    В шаблоне отображаем изображение, имя и описание (обрезанное до 100 символов).
    """
    products = Product.objects.select_related('category').order_by('-created_at')
    return render(request, 'home.html', {'products': products})

def product_detail(request, pk):
    """
    Страница одного товара: принимает pk, получает объект через ORM и рендерит шаблон.
    """
    product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
    return render(request, 'product_detail.html', {'product': product})



