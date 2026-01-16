# coding: utf-8
from products_proj.models import Category, Product
c1 = Category.objects.create(name='Electronics', description='Электроника')
p = Product.objects.create(name='Laptop', description='Хороший ноутбук ...', category=c, price_for_unit=12345.6)
p = Product.objects.create(
    name='Laptop',
    description='Хороший ноутбук ...',
    category=c1, 
    price=12345.67
)
p = Product.objects.create(
    name='Laptop',
    description='Хороший ноутбук ...',
    category=c1, 
    price_for_unit=12345.67 
)
