from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from . import views

urlpatterns = [
    path('users/', views.CreateUser.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='access_token'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh_token'),
]
