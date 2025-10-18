from django.urls import path

from .views import UserLoginAPIView, UserRegisterAPIView

app_name = "users"

urlpatterns = [
    path("register/", UserRegisterAPIView.as_view(), name="register"),
    path("login/", UserLoginAPIView.as_view(), name="login"),
]
