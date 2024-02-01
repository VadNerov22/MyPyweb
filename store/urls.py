from django.urls import path
from .views import ProductSingleView, CartView, ShopView, CartViewSet, WishlistView, WishListViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'cart', CartViewSet)
router.register(r'wishlist', WishListViewSet)

app_name = 'store'

urlpatterns = [
    path('', ShopView.as_view(), name='shop'),
    path('cart/', CartView.as_view(), name='cart'),
    path('product/<int:id>/', ProductSingleView.as_view(), name='product'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('wishlist/create/', WishlistView.add_wish_product, name='add_wish_product'),
    path('wishlist/delete/', WishlistView.dell_wish_product, name='dell_wish_product'),
]