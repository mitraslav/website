from django.core.cache import cache
from products_proj.models import Product
from django.conf import settings

CATEGORY_PRODUCTS_CACHE_TIMEOUT = 60 * 15

def get_products_by_category(category_id):
    """Возвращает список Product в категории, с кешированием."""
    cache_key = f'category_products_{category_id}'
    products = None
    if settings.CACHE_ENABLED:
        products = cache.get(cache_key)

    if products is None:
        qs = Product.objects.filter(category_id=category_id, is_published=True) \
            .select_related('category') \
            .order_by('-created_at')
        # materialize queryset - хранится в кеше как список объектов (pickled)
        products = list(qs)
        if settings.CACHE_ENABLED:
            cache.set(cache_key, products, CATEGORY_PRODUCTS_CACHE_TIMEOUT)
    return products

def invalidate_category_cache(category_id):
    from django.conf import settings
    key = f'category_products_{category_id}'
    if settings.CACHE_ENABLED:
        cache.delete(key)
