from django.urls import reverse
from django.test import TestCase
from datetime import datetime
from pytz import UTC
from Farm.models import (ProductType,
                         Product,
                         Basket,
                         User,
                         Order, )


class FarmModelsTestCase(TestCase):
    def setUp(self):
        ProductType.objects.create(
            product_type='Fruits', )
        ProductType.objects.create(
            product_type='Vegetables', )
        Product.objects.create(
            product='Apple',
            price='2.56',
            type=ProductType.objects.get(id=1), )
        Product.objects.create(
            product='Orange',
            price='1.07',
            type=ProductType.objects.get(id=2), )
        Product.objects.create(
            product='Banana',
            price='2.21',
            type=ProductType.objects.get(id=1), )
        Basket.objects.create(
            product_id=Product.objects.get(id=1).id,
            product_type=Product.objects.get(id=1).type,
            product=Product.objects.get(id=1).type,
            price=Product.objects.get(id=1).price,
            amount=2,
            cost=2 * Product.objects.get(id=1).price, )
        Basket.objects.create(
            product_id=Product.objects.get(id=2).id,
            product_type=Product.objects.get(id=2).type,
            product=Product.objects.get(id=2).type,
            price=Product.objects.get(id=2).price,
            amount=2,
            cost=2 * Product.objects.get(id=2).price, )
        User.objects.create(
            username='alex',
            password='1234567890',
            first_name='Alex',
            last_name='Orlovich',
            email='maksimdulchevskiy@mail.ru',
            phone_number='+375(29)348-48-28',
            address='Sukharevskaya 27, 49',
            login=1, )
        Order.objects.create(
            user_type=User,
            first_name=User.objects.get(id=1).first_name,
            last_name=User.objects.get(id=1).last_name,
            email=User.objects.get(id=1).email,
            phone_number=User.objects.get(id=1).phone_number,
            address=User.objects.get(id=1).address,
            order_date=datetime.now(tz=UTC),
            delivery_date=datetime(2022, 12, 31, 15, 16, tzinfo=UTC),
            comment='Good day, sir.',
            user=User.objects.get(id=1), )

    def test_create(self):
        # проверка на успешное создание объектов всех типов.
        product_type_object = ProductType.objects.filter(id=1).first()
        product_object = Product.objects.filter(id=1).first()
        basket_object = Basket.objects.filter(id=1).first()
        user_object = User.objects.filter(id=1).first()
        order_object = Order.objects.filter(id=1).first()
        self.assertNotEqual(product_type_object, None)
        self.assertNotEqual(product_object, None)
        self.assertNotEqual(basket_object, None)
        self.assertNotEqual(user_object, None)
        self.assertNotEqual(order_object, None)

    def test_get(self):
        # проверка отображения всех страниц.
        response1 = self.client.get('/')
        self.assertEqual(response1.status_code, 200)
        response2 = self.client.get('/Chocolate')
        self.assertEqual(response2.status_code, 200)
        response3 = self.client.get('/sign_in')
        self.assertEqual(response3.status_code, 200)
        response4 = self.client.get('/registration')
        self.assertEqual(response4.status_code, 200)
        response5 = self.client.get('/checkout')
        self.assertEqual(response5.status_code, 200)

    def test_post_home_sign_out(self):
        # проверка выхода пользователя и перенаправления на страницу, откуда был выход совершен.
        user = User.objects.get(id=1)
        self.assertEqual(user.login, 1)
        response = self.client.post('/', {}, HTTP_REFERER='/checkout')
        user = User.objects.get(id=1)
        self.assertEqual(user.login, 0)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/checkout')

    def test_post_sign_in(self):
        # проверка авторизации пользователя.
        user = User.objects.filter(id=1)
        user.update(login=0)
        self.assertEqual(user.first().login, 0)
        response = self.client.post('/sign_in/', {'username': 'alex', 'password': '1234567890'})
        user = User.objects.get(id=1)
        self.assertEqual(user.login, 1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/sign_in/')

    def test_post_registration(self):
        # проверка регистрации пользователя и перенаправления на страницу авторизации.
        user = User.objects.filter(username='maxim').first()
        self.assertEqual(user, None)
        response = self.client.post('/registration/', {
            'first_name': 'Alexey',
            'last_name': 'Orlovich',
            'email': 'alex.orlovich@gmail.com',
            'phone_number': '+375(29)348-48-28',
            'address': 'Sukharevskaya 27, 49',
            'username': 'Alexey',
            'password': '1234567890',
            'conf_password': '1234567890',
        })
        user = User.objects.filter(username='Alexey').first()
        self.assertNotEqual(user, None)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/sign_in/')

    def test_post_add_to_basket(self):
        # проверка добавления в корзину сладости количеством 0 шт. на странице сладости.
        response = self.client.post('/add/3', {'amount': '0'}, HTTP_REFERER='/Fruits')
        product = Basket.objects.filter(id=3).first()
        self.assertEqual(product, None)
        self.assertEqual(response.status_code, 302)
        # проверка добавления в корзину сладости количеством 5 шт. на странице сладости.
        response = self.client.post('/add/3', {'amount': '5'}, HTTP_REFERER='/Fruits')
        product = Basket.objects.get(id=3)
        self.assertEqual(product.amount, 5)
        self.assertEqual(response.status_code, 302)
        # проверка изменения количества сладости в корзине с 5 до 10 шт. на странице сладости.
        response = self.client.post('/add/3', {'amount': '10'}, HTTP_REFERER='/Fruits')
        product = Basket.objects.get(id=3)
        self.assertEqual(product.amount, 10)
        self.assertEqual(response.status_code, 302)
        # проверка изменения количества сладости в корзине 10 до 0 шт. на странице сладости.
        response = self.client.post('/add/3', {'amount': '0'}, HTTP_REFERER='/Fruits')
        product = Basket.objects.get(id=3)
        self.assertEqual(product.amount, 10)
        self.assertEqual(response.status_code, 302)
        # проверка изменения количества сладости в корзине с 10 до 5 шт. на странице корзины.
        response = self.client.post('/add/3', {'amount': '5'}, HTTP_REFERER='/checkout')
        product = Basket.objects.get(id=3)
        self.assertEqual(product.amount, 5)
        self.assertEqual(response.status_code, 302)
        # проверка изменения количества сладости в корзине с 5 до 0 шт. на странице корзины.
        response = self.client.post('/add/3', {'amount': '0'}, HTTP_REFERER='/checkout')
        product = Basket.objects.filter(id=3).first()
        self.assertEqual(product, None)
        self.assertEqual(response.status_code, 302)

    def test_post_del_from_basket(self):
        # проверка удаления сладости в корзине.
        response = self.client.post('/del/1', {}, HTTP_REFERER='/checkout')
        product = Basket.objects.filter(id=1).first()
        self.assertEqual(product, None)
        self.assertEqual(response.status_code, 302)
