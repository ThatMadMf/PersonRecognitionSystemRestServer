from django.urls import path

from server import views

urlpatterns = [
    path('users', views.Users.as_view()),

    path('user-face-encodings', views.UserFaceEncodings.as_view()),

    path('recognition', views.FaceRecognition.as_view()),
]
