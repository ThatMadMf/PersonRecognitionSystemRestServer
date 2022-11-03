from django.urls import path

from server import views

urlpatterns = [
    path('users', views.Users.as_view()),

    path('perform-recognition', views.FrameRecognition.as_view()),
]
