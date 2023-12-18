import json
import socket
from random import choice
from django.forms import model_to_dict
from django.contrib.auth.models import User as SuperUser


def generate_logo():
    logo_names = ['logo_2_1.png', 'logo_2_2.png', 'logo_2_3.png']
    logo_name = choice(logo_names)
    return logo_name


def products_to_json(products):
    products = [model_to_dict(product) for product in products]
    products_dict = {}
    for product in products:
        product_id = product['product_id']
        del product['id']
        del product['product_id']
        products_dict[product_id] = product
    json_products = json.dumps(products_dict)
    return json_products


def check_connection():
    try:
        socket.gethostbyaddr('www.yandex.ru')
    except socket.gaierror:
        return False
    return True


def get_superuser_email():
    superusers_emails = SuperUser.objects.filter(is_superuser=True).values_list('email')
    return superusers_emails[0][0]


def make_list_of_lists(iter_object, row, amount):
    list_of_lists = []
    count = 1
    for i, elem in enumerate(iter_object):
        if count == 1:
            line = []
        line.append(elem)
        count += 1
        if count > row:
            count = 1
            list_of_lists.append(line)
            line = []
        elif i + 1 == amount:
            list_of_lists.append(line)
    return list_of_lists


def order_message(order, products, order_total):
    message = f'Hello, {order.first_name}!\n\n' \
              f'Your order was successfully accepted {order.order_date.date()} at ' \
              f'{(order.order_date.time()).replace(microsecond=0)}\n\n' \
              'Delivery date:' + f'{order.delivery_date.date()} at {order.delivery_date.time()}'.rjust(45, '.') + \
              '\nDelivery address:' + f'{order.address}'.rjust(42, '.') + '\n' \
              'Phone number:' + f'{order.phone_number}'.rjust(46, '.') + '\n\n\n\n\n' \
              'Your order:\n' \
              '\nProduct'.ljust(53, ' ') + 'Price'.rjust(8, ' ') + 'Amount'.rjust(8, ' ') + 'Cost'.rjust(8, ' ') + \
              '\n' + ''.rjust(59, '-') + '\n'
    for product in products:
        message += f'{product.product}'.ljust(35, ' ') + \
                   f'{product.price}'.rjust(8, ' ') + \
                   f'{int(product.amount)}'.rjust(8, ' ') + \
                   f'{product.cost}'.rjust(8, ' ') + '\n'
    message += ''.rjust(59, '-') + '\n' + f'Order Total: {order_total} BYN'.rjust(59, ' ') + '\n\n\n' \
               'Comment:' + '\n\n'
    comment = order.comment.split()
    row_len = 0
    for word in comment:
        row_len += len(word)
        if row_len < 44:
            message += f'{word} '
        else:
            message += f'{word}\n'
            row_len = 0
    return message
