# video_clipper/urls.py
from django.urls import path
from .views import video_clipper_view

urlpatterns = [
    path('', video_clipper_view, name=''),
]    
