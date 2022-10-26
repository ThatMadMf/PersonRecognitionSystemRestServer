from django.urls import path

from server import views

urlpatterns = [
    path('perform-recognition', views.PerformRecognition.as_view()),
]
