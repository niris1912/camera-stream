from django.urls import path
from . import views

urlpatterns = [
    path('camera/', views.camera_stream, name='camera_stream'),
    path('video/', views.video_stream, name='video_stream'),
    path('capture/', views.capture_stream, name='capture_stream'),
    # Define other URL patterns for your app...
]
