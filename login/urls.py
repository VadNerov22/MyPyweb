from django.urls import path
from .views import LoginView, LogoutView, CreateAccountView


app_name = 'login'

urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('create/', CreateAccountView.as_view(), name="create"),
    path('logout/', LogoutView.as_view(), name="logout"),
]