from django.urls import path
from api import views

urlpatterns = [
    path('contents/', views.PostList.as_view()),
    path('contents/<int:pk>', views.PostDetail.as_view()) # id = author_id인 user의 posts들 가져오기
    ]