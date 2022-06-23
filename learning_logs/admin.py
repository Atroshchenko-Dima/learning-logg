from django.contrib import admin
# Register your models here.

from .models import Entry, Topic # импортирует регистрируемую модель, точка перед моделс означает что файл models.py в этом же каталоге
admin.site.register(Topic) # сообщает джанго, что управление моделью должно осуществляться через административный сайт
admin.site.register(Entry)