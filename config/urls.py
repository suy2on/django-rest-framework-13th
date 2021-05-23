"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings
# jwt token
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/token/', obtain_jwt_token),  # JWT 토큰을 발행
    path('auth/token/verify/', verify_jwt_token), # JWT 토큰이 유효한지 검증
    path('au/token/refresh/', refresh_jwt_token), # JWT 토큰을 갱신할 때 사용
    path('api/', include('api.urls'))
]

# 이미지 url설정
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)