# youtube_video_clipper/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('admin:index')),
    path('admin/', admin.site.urls),
    path('clip/', include('video_clipper.urls')),
]
