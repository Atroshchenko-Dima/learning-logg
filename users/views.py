from django.shortcuts import render, redirect
from django.contrib.auth import login # для выполнения входа пользователя, если регистр. информация верна
from django.contrib.auth.forms import UserCreationForm

def register(request):
    # Регистрирует нового пользователя
    if request.method != 'POST': # определяем запрос GET(запросил ли пользователь пустую форму) or Post(предлагает обработать заполненную форму)
        # создается пустая форма регистрации
        form = UserCreationForm() # экземпляр не содержащий данных
    else:
        # отправлены данные РОST, обработать данные
        form = UserCreationForm(data = request.POST) 
        if form.is_valid(): # проверяет что все обязательные поля были заполнены, пароли совпадают, имя содержит правильные символы
            new_user = form.save() # если введенные данные верны, сохраняем в базу данных
            # Выполнение входа и перенаправление на домашнюю страницу
            login(request, new_user)
            return redirect('learning_logs:index') # после сохраненных данных страницу можно покинуть. redirect перенапрявляет браузер на домашнюю страницу
    # вывести пустую или недействительную форму
    context = {'form' : form}
    return render(request, 'registration/register.html', context)

