from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic # форма создается на базе модели топик, а на ней размещается только поле текст
        fields = ['text']
        labels = {'text': ''} # приказывает джанго не генерировать подпись для текстового поля

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text'] # снова назначается пустая надпись
        labels = {'text': 'Entry:'} 
        widgets = {'text': forms.Textarea(attrs={'cols':80})} # вместо стандартной ширины текстовой области = 40 столбцов, делаем 80
        