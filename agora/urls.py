from django.urls import path
from . import views

urlpatterns = [
    path('get-agora-token/', views.AgoraTokenView.as_view(), name='get-agora-token'),
    path('get-call-info/', views.GetConsultationView.as_view(), name='get_call_info'),
]
