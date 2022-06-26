# Определяет схемы URL для learning_logs.
from django.urls import path # для связывания URL с представлениями
from . import views # Точка приказывает питону импортировать представления из каталога, в котором находится текущий модуль urls.py

app_name = 'learning_logs' # помогает питону отличить urls.py от одноименных файлов в других приложениях проекта
urlpatterns = [ 
    # Переменная в этом модуле представляет с собой список страниц, которые могут запрашиваться из приложения learning_logs
    # домашняя страница
    path('', views.index, name = 'index'),
    # страница со списком всех тем
    path('topics/', views.topics, name = 'topics'),
    # страница с подробной информацией по отдельной теме
    path('topics/<int:topic_id>/', views.topic, name = 'topic'),
    # страница для добавления новой темы
    path('new_topic/', views.new_topic, name = 'new_topic'),
    # страница для добавления новой записи
    path('new_entry/<int:topic_id>/', views.new_entry, name = 'new_entry'),
    # страница для добавления новой записи
    path('edit_entry/<int:entry_id>/', views.edit_entry, name = 'edit_entry'),
    # Удаление записи из топика
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    # Удаление темы
    path('delete_topic/<int:topic_id>/', views.delete_topic, name='delete_topic'),
]