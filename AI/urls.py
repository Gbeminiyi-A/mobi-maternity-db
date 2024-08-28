from .views import *
from django.urls import path

urlpatterns = [
    path('ai-response/', AiResponseView.as_view(), name='ai-response'),
]