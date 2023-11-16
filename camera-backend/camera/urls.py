from django.urls import path
from . import views

urlpatterns = [
    path('camera_stream/', views.camera_stream, name='camera_stream'),
    # Define other URL patterns for your app...
]
