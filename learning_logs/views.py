from .models import Topic, Entry # импортируем модель связанную с нужными данными
from .forms import TopicForm, EntryForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404


def index(request):
    # Домашняя страница приложения Learning_logs
    return render(request, 'learning_logs/index.html')

@login_required # джанго запускает код, только если пользователь вошел в систему, если не вошел то перенаправляет на страницу входа
def topics(request):
    # Выводит список тем
    topics = Topic.objects.filter(owner=request.user).order_by('date_added') # Выдается запрос к базе данных на получение объектов Topic, отсортированных по атрибуту date_added.
    context = {'topics' : topics} # Определяется контекст, который будет передаваться шаблону
    return render(request, 'learning_logs/topics.html', context) 

@login_required
def topic(request, topic_id):
    """Выводит одну тему и все ее записи."""
    topic = get_object_or_404(Topic, id=topic_id)  # get используется для получения темы
    # Проверка того, что тема принадлежит текущему пользователю
    _check_topic_owner(request, topic)
    entries = topic.entry_set.order_by('-date_added') # загружаются записи, связанные с данной темой и они упорядочиваются по значению data_added. - означает сортировку в обратном порядке, т.е последнии записи оказываются на первых местах
    context = {'topic': topic, 'entries': entries} # Темы и записи сохраняются в словаре context, который передается шаблону topic.html
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    # Определяет новую тему
    if request.method != 'POST': # определяем запрос GET(запросил ли пользователь пустую форму) or Post(предлагает обработать заполненную форму)
        # данные не отправлялись, создается пустая форма
        form = TopicForm() # создается пустая форма, которая заполняется пользователем
    else:
        # отправлены данные РОST, обработать данные
        form = TopicForm(data = request.POST) # создаем экземпляр топикформ и передаем ему данные, заполненные пользователем, хранящиеся в request.post
        if form.is_valid(): # проверяет что все обязательные поля были заполнены, а введенные данные соответсвуют типам полей - например что длина текста меньше 200 символов, как было указано в models.py
            new_topic = form.save(commit=False)
            new_topic.owner = request.user # атрибуту темы присваеватся текущий пользователь
            new_topic.save() # записывает данные из формы в базу данных
            return redirect('learning_logs:topics') # после сохраненных данных страницу можно покинуть. redirect перенапрявляет браузер на страницу топикс, где пользователь увидит введенную им тему в общем списке тем
    # вывести пустую или недействительную форму
    context = {'form' : form}
    return render(request, 'learning_logs/new_topic.html', context) # страница строится на шаблоне new_topic.html   

@login_required
def new_entry(request, topic_id):
    """Добавляет новую запись по конкретной теме."""
    topic = get_object_or_404(Topic, id=topic_id)
    _check_topic_owner(request, topic)
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = EntryForm() 
    else:
        # Отправлены данные POST; обработать данные создавая экземпляр EntryForm заполненный данными из объекта request.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False) # если данные корректны, необходимо задать атрибут topic объекта записи перед сохранением его в базе данных. При вызове save включаем аргумент commit=False для того чтобы создать новый объект записи и сохранить его в new_entry, не сохраняя пока в базе данных
            new_entry.topic = topic # Присваиваем атрибуту topic тему, прочитанную из базы данных в начале функции
        if topic.owner != request.user:
            raise Http404
        else:
            new_entry.save() # вызываем save без аргументов. Запись сохраняется в базе данных с правильно ассоциированной темой
            return redirect('learning_logs:topic', topic_id=topic_id)
 
    # Вывести пустую или недействительную форму.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    # редактирует существующую запись
    entry = get_object_or_404(Entry, id=entry_id) # получаем объект записи, который пользователь хочет изменить, и тему, связанную с этой записью
    topic = entry.topic
    _check_topic_owner(request, topic)
    if request.method != 'POST':
        # исходный запрос, форма заполняется данными текущей записи
        form = EntryForm(instance=entry) # instance=entry - приказывает создать форму, заранее заполненную информацией из существующего объекта записей
    else:
        # отправленны данные POST; обработать данные создавая экземпляр EntryForm заполненный данными из объекта request
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    context = {'entry' : entry,'topic' : topic, 'form' : form}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required()
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    _check_topic_owner(request, entry.topic)
    entry.delete()
    return redirect('learning_logs:topic', topic_id=entry.topic.id)

@login_required()
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    _check_topic_owner(request, topic)
    topic.delete()
    return redirect('learning_logs:topics')

def _check_topic_owner(request, topic):
    if topic.owner != request.user:
        raise Http404