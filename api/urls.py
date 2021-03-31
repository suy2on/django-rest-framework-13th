from django.urls import path
from api import views

urlpatterns = [
    path('post/', views.post_list)
]