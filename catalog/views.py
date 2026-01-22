from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from products_proj.models import Product
from .forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import IsOwnerMixin, CanDeleteMixin

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.select_related('category').order_by('-created_at')

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    login_url = reverse_lazy('users:login')

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        # привязываем владельца
        form.instance.owner = self.request.user
        # по умолчанию сделать продукт не опубликованным
        form.instance.is_published = False
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, IsOwnerMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

class ProductDeleteView(LoginRequiredMixin, CanDeleteMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

def home(request):
    """
    Контроллер главной страницы. Рендерит templates/home.html через render.
    Зарегистрирован на адрес '/'
    """
    return render(request, 'home.html', {})


def contacts(request):
    """
    Обработка контактов без использования django.forms.
    - Валидируем простыми проверками
    - При ошибках возвращаем те же значения в поля и показываем ошибки
    - При успешной отправке показываем сообщение об успехе
    """
    errors = {}
    success = False
    name = email = message = ''

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if not name:
            errors['name'] = 'Введите имя'
        if not email or '@' not in email:
            errors['email'] = 'Введите корректный e-mail'
        if not message:
            errors['message'] = 'Введите сообщение'

        if not errors:
            success = True
            name = email = message = ''

    context = {'errors': errors, 'success': success, 'name': name, 'email': email, 'message': message}
    return render(request, 'catalog/contacts.html', context)