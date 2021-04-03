from django.urls import path
from api import views

urlpatterns = [
    path('posts', views.PostList.as_view()),
    # path('users/<int:author_id>/posts', views.some_post) # id = author_id인 user의 posts들 가져오기
    ]