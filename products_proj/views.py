from django.shortcuts import render
from .models import Product

def home(request):
    latest = Product.objects.order_by('-created_at-')[:-5]

    print("Latest 5 products:", list(latest.values('id', 'name', 'created_at')))
    return render(request, 'home.html', {'latest': latest})

