# Определяет схемы URL для пользователей
from django.urls import path, include # URL адреса включающие в себя login and logout
from . import views

app_name = 'users'
urlpatterns = [
    # Включить URL авторизации по умолчанию
    path('', include('django.contrib.auth.urls')),
    # Страница регистрации
    path('register/', views.register, name = 'register'),
]