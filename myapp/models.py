from django.conf import settings
from django.db import models

class Question(models.Model):
    question = models.TextField(default='')
    answer = models.TextField(default='')
    asked_date = models.IntegerField(default=0)

    def get(self):
        return self

    def get_question(self):
        return self.question

    def get_answer(self):
        return self.answer

    def set_date(self):
        return self.asked_date

    def get_date(self):
        return self.asked_date

    def __str__(self):
        return self.question