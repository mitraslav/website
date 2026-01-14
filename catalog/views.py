from django.shortcuts import render

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