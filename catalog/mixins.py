from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy

class IsOwnerMixin(UserPassesTestMixin):
    """
        Доступ разрешён только владельцу объекта (obj.owner == request.user).
    """
    login_url = reverse_lazy('users:login')
    raise_exception = False

    def test_func(self):
        obj = self.get_object()
        user = getattr(self.request, 'user', None)
        return user.is_authenticated and obj.owner == user

    def handle_no_permission(self):
        return super().handle_no_permission()


class CanDeleteMixin(UserPassesTestMixin):
    """
        Разрешение удалить: если пользователь — владелец объекта ИЛИ имеет право delete_product
        или наше кастомное право can_unpublish_product (в зависимости от app_label).
    """

    login_url = reverse_lazy('users:login')
    raise_exception = False

    def test_func(self):
        obj = self.get_object()
        user = getattr(self.request, 'user', None)
        if not user or not user.is_authenticated:
            return False
        if obj.owner == user:
            return True
        if user.has_perm('products_proj.delete_product'):
            return True
        if user.has_perm('products_proj.can_unpublish_product'):
            return True
        return False
