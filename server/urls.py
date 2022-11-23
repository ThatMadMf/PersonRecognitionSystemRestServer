from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from server import views

urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('me', views.Me.as_view()),

    path('users', views.Users.as_view()),

    path('user-face-encodings', views.UserFaceEncodings.as_view()),

    path('capture-sessions', views.CaptureSessions.as_view()),
    path('capture-sessions/<int:session_id>/complete', views.CompleteCaptureSession.as_view()),

    path('recognition/<str:image_type>', views.FaceRecognition.as_view()),

    path('session-frames', views.SessionFrames.as_view()),
]
