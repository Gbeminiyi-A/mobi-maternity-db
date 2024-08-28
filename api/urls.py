from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenRefreshView)

from . import views

router = routers.DefaultRouter()

app_name = 'api'

router.register('user-create', views.UserRegistrationViewSet)
router.register('user-detail', views.UserDetailViewSet)
router.register('health-info/create', views.HealthInfoRegistrationViewSet, basename='health-info-create')
router.register('health-info', views.HealthDetailViewSet, basename='health-info')
router.register('health-worker/create', views.HealthWorkerInfoRegistrationViewSet, basename='health-worker-create')
router.register('health-worker', views.HealthWorkerDetailViewSet, basename='health-worker')
router.register('worker-list', views.HealthWorkerListViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.BlacklistRefreshView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
