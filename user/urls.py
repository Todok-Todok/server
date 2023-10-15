from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view()),
    path('base/login/', views.LoginAPIView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()), # 토큰 재발급
    # 소셜로그인
    path('google/login/', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name='google_callback'),  
    path('google/login/finish/', views.GoogleLogin.as_view(), name='google_login_todjango'),
]