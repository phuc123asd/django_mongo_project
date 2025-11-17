# api/urls.chatbot.py
from django.urls import path
from api.views.chatbot import *

urlpatterns = [
    path('', chatbot, name='chatbot_view'),
]