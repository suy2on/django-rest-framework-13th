from django.urls import path
from api import views

from rest_framework import routers
from .views import PostViewSet, ProfileViewSet

router = routers.DefaultRouter()
router.register(r'contents', PostViewSet)   # register()함으로써 두 개의 url 생성
router.register(r'users', ProfileViewSet)

urlpatterns = router.urls

