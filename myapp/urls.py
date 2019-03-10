from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('question', views.question, name='question'),
    path('answer/<int:pk>/', views.answer, name='answer'),
    path('all', views.all, name='all'),
    path('question_result', views.question_result, name='question_result'),
]