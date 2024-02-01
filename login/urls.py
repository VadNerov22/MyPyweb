from django.urls import path
from .views import LoginView, LogoutView, CreateAccountView


app_name = 'login'

urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('create/', CreateAccountView.as_view(), name="create"),
    path('logout/', LogoutView.as_view(), name="logout"),
    # path('create/', WishlistView.add_wish_product, name='add_wish_product'),
    # path('delete/', WishlistView.dell_wish_product, name='dell_wish_product'),
]