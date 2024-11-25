from django.urls import path
from . import reply_factory

urlpatterns = [
    path('', reply_factory.start_quiz, name='start_quiz'),

]
