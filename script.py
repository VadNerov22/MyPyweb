import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

django.setup()

from store.models import Product, Category

if __name__ == "__main__":
    # Создание объекта, затем его сохранение
    category = Category.objects.get(name='Vegetables')
    obj = Product(name='Carrots', description='Морковь', price=120,
                  image='static/products/product-7.jpg',
                  category=category)
    obj.save()
    # Создание с сохранением
    obj = Product.objects.create(name='Fruit Juice',
                                 description='Фруктовый сок',
                                 price=120,
                                 image='static/products/product-8.jpg',
                                 category=Category.objects.get(name='Juice'))
    # Групповое сохранение(сохранение блока информации)
    data = ({'name': 'Onion',
             'price': 120.00,
             'description': "Лук",
             'image': 'static/products/product-9.jpg',
             'category': 'Vegetables'},
            {'name': 'Apple',
             'price': 120.00,
             'description': "Яблоко",
             'image': 'static/products/product-10.jpg',
             'category': 'Fruits'},
            {'name': 'Garlic',
             'price': 120.00,
             'description': "Чеснок",
             'image': 'static/products/product-11.jpg',
             'category': 'Vegetables'},
            )
    # Подгрузим объекты для категорий
    categ = {'Fruits': Category.objects.get(name='Fruits'),
             'Vegetables': Category.objects.get(name='Vegetables'),
             }
    # Создадим объекты для записи группой и запишем их
    objects_to_create = [Product(name=val['name'],
                                 description=val['description'],
                                 price=val['price'],
                                 image=val['image'],
                                 category=categ[val['category']]) for val in data]

    Product.objects.bulk_create(objects_to_create)

