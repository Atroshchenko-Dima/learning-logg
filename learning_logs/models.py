from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    # Тема которую изучает пользователь
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        #Возвращает строковое представление модели
        return self.text

class Entry(models.Model): # наследует от базового класса Model, как и класс Топик(выше)
    # Информация изученная пользователем по теме
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE) # "Внешний ключ" содержит ссылку на другую запись в базе данных
    # on_delete=models.CASCADE -(каскадное удаление) сообщает django, что при удалении темы все записи, связанные с этой темой, также должны быть удалены
    text = models.TextField() # размер записей не ограничевается
    date_added = models.DateTimeField(auto_now_add=True) # отображение записей в порядке их создания

    class Meta:
        verbose_name_plural = 'entries' # приказывает джанго использовать форму множественного числа при обращении более чем к 1ой записи
    def __str__(self):
        if len(self.text) > 50:
        # Возвращает строковое представление модели
            return f'{self.text[:50]}...'
        else:
            return f'{self.text}'
                  # сообщает джанго какая информация должна отображаться при обращении к отдельным записям.
        # приказываем выводить только первые 50 символов, затем многоточие(признак вывода неполного текста)

