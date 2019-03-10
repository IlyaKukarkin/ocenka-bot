from django import forms

from .models import Question

class PostForm(forms.Form):
    your_question = forms.CharField(label='Ваш вопрос', max_length=100)