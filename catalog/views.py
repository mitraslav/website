from django.shortcuts import render, redirect

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

    # Значения для подстановки в поля (чтобы пользователь не терял введённое)
    name = ''
    email = ''
    message = ''

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        # Простая валидация
        if not name:
            errors['name'] = 'Введите имя'
        if not email:
            errors['email'] = 'Введите e-mail'
        elif '@' not in email or len(email) < 5:
            errors['email'] = 'Введите корректный e-mail'
        if not message:
            errors['message'] = 'Введите сообщение'

        # Если ошибок нет — можно сохранить/отправить/обработать
        if not errors:
            # Здесь можно: сохранить в базу, отправить на почту и т.д.
            success = True

            # Очистим поля (чтобы показать пустую форму). Можно не очищать, если нужно.
            name = email = message = ''

            # Хорошая практика — redirect после POST (POST-redirect-GET),
            # чтобы при перезагрузке страницы не было повторной отправки формы.
            # Ниже приводим вариант с redirect и сообщением через query-параметр.
            # Но для простоты сейчас просто показываем success на той же странице.
            # return redirect('catalog:contacts')  # если хотите redirect

    context = {
        'errors': errors,
        'success': success,
        'name': name,
        'email': email,
        'message': message,
    }
    return render(request, 'contacts.html', context)
