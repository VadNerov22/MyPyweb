import self as self
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status

from .models import Cart, Product, Category, Wishlist
from .serializers import CartSerializer, WishlistSerializer
from .views import CartViewSet, WishListViewSet


class CartViewSetTestCase(TestCase):
    """
    Тестирование объекта CartViewSet

    При тестировании проверяем правильность создания объектов, а также
    правильность отрабатывания методов:
       create (test_create_cart_item),
       update (test_update_cart_item),
       delete (test_delete_cart_item).
    """
    fixtures = ['testdata.json']
    def setUp(self):
       """
       Инициализация параметров перед запуском каждого теста (Django очищает БД
       перед каждым тестом, поэтому в начале каждого теста создаются данные
       необходимые для теста)
       """

       # Создание объекта моделирующего отправление запроса
       self.factory = APIRequestFactory()

       self.user = User.objects.first()
       self.product = Product.objects.first()

    def test_create_cart_item(self):
       # Отправляем запрос на адрес /carts/ с данными
       request = self.factory.post('/carts/', {'product': self.product.id})
       # Записываем пользователя в запрос (имитирование действия промежуточного ПО в Django)
       request.user = self.user
       # Инициализуем вызов POST запроса в представлении
       view = CartViewSet.as_view({'post': 'create'})
       # Передаём запрос в представление и получаем результат от этого представления
       response = view(request)
       # Проводим проверки тех действий, что сделало представление
       self.assertEqual(response.status_code, status.HTTP_201_CREATED)
       self.assertEqual(response.data['message'], 'Product added to cart')
       self.assertEqual(Cart.objects.count(), 1)

    def test_update_cart_item(self):
       cart_item = Cart.objects.create(user=self.user, product=self.product)
       request = self.factory.put(f'/carts/{cart_item.id}/', {'quantity': 5})
       request.user = self.user
       view = CartViewSet.as_view({'put': 'update'})

       response = view(request, pk=cart_item.id)
       self.assertEqual(response.status_code, status.HTTP_201_CREATED)
       self.assertEqual(response.data['message'], 'Product change to cart')

       cart_item.refresh_from_db()
       # Изменение было внесено непосредственно в базу данных, а не в объект
       # Python, refresh_from_db() гарантирует, что объект cart_item отобразит
       # актуальные данные из базы данных, что важно для правильного
       # проведения последующих проверок в вашем тесте.
       self.assertEqual(cart_item.quantity, 5)

    def test_delete_cart_item(self):
       cart_item = Cart.objects.create(user=self.user, product=self.product)
       request = self.factory.delete(f'/carts/{cart_item.id}/')
       request.user = self.user
       view = CartViewSet.as_view({'delete': 'destroy'})

       response = view(request, pk=cart_item.id)
       self.assertEqual(response.status_code, status.HTTP_201_CREATED)
       self.assertEqual(response.data['message'], 'Product delete from cart')
       self.assertEqual(Cart.objects.count(), 0)


class CartSerializerTestCase(TestCase):
    """
    Пример проверки сериализатора
    """
    fixtures = ['testdata.json']

    def setUp(self):
       self.user = User.objects.first()
       self.product = Product.objects.first()
       self.cart_item = Cart.objects.create(user=self.user, product=self.product)

    def test_cart_serializer(self):
       serializer = CartSerializer(instance=self.cart_item)
       expected_data = {
           'id': self.cart_item.id,
           'user': self.user.id,
           'quantity': self.cart_item.quantity,
           'product': self.product.id,
       }

       # Проверка, что на выходе сериализатора данные соответствуют нужным
       self.assertEqual(serializer.data, expected_data)


class WishListViewSetTestCase(TestCase):
    """
    Тестирование объекта WishListViewSet

    При тестировании проверяем правильность создания объектов и отрабатывания методов:
       create (test_create_wish_item),
       update (test_update_wish_item),
       delete (test_delete_wish_item).
    """
    fixtures = ['testdata.json']
    def setUp(self):

       # Создание объекта моделирующего отправление запроса
       self.factory = APIRequestFactory()

       self.user = User.objects.first()
       self.product = Product.objects.first()

    def test_create_wish_item(self):
       # Отправляем запрос на адрес /wishlist/ с данными
       request = self.factory.post('/wishlist/', {'product': self.product.id})
       # Записываем пользователя в запрос
       request.user = self.user
       # Инициализуем вызов POST запроса в представлении
       view = WishListViewSet.as_view({'post': 'create'})
       response = view(request)
       # Проводим проверки тех действий, что сделало представление
       self.assertEqual(response.status_code, status.HTTP_201_CREATED)
       self.assertEqual(response.data['message'], 'Product added to Wishlist')
       self.assertEqual(Wishlist.objects.count(), 1)

    def test_update_wish_item(self):
       wish_item = Wishlist.objects.create(user=self.user, product=self.product)
       request = self.factory.put(f'/wishlist/{wish_item.id}/', {'quantity': 5})
       request.user = self.user
       view = WishListViewSet.as_view({'put': 'update'})

       response = view(request, pk=wish_item.id)
       self.assertEqual(response.status_code, status.HTTP_201_CREATED)
       self.assertEqual(response.data['message'], 'Product change in Wishlist')

       wish_item.refresh_from_db()
       self.assertEqual(wish_item.quantity, 5)

    def test_delete_wish_item(self):
       wish_item = Wishlist.objects.create(user=self.user, product=self.product)
       request = self.factory.delete(f'/wishlist/{wish_item.id}/')
       request.user = self.user
       view = WishListViewSet.as_view({'delete': 'destroy'})

       response = view(request, pk=wish_item.id)
       self.assertEqual(response.status_code, status.HTTP_201_CREATED)
       self.assertEqual(response.data['message'], 'Product delete from Wishlist')
       self.assertEqual(Wishlist.objects.count(), 0)


class WishlistSerializerTestCase(TestCase):
    """
    Проверка сериализатора
    """
    fixtures = ['testdata.json']

    def setUp(self):
       self.user = User.objects.first()
       self.product = Product.objects.first()
       self.wish_item = Wishlist.objects.create(user=self.user, product=self.product)

    def test_wish_serializer(self):
       serializer = WishlistSerializer(instance=self.wish_item)
       expected_data = {
           'id': self.wish_item.id,
           'user': self.user.id,
           'quantity': self.wish_item.quantity,
           'product': self.product.id,
       }

       # Проверка, что на выходе сериализатора данные соответствуют нужным
       self.assertEqual(serializer.data, expected_data)
