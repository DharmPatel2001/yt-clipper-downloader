# youtube_video_clipper/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('video_clipper.urls')),
    path('admin/', admin.site.urls),
]
