from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('images', views.ImageAPIView)

urlpatterns = [
    path('', views.api_overview, name='home'),
]

urlpatterns += router.urls
