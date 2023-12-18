from django.shortcuts import render
from My_Final.funcs import generate_logo
from Farm.models import (ProductType,
                               User, )


def product_page(request, product_type):
    product_types = ProductType.objects.filter().values_list()
    product_types = [type[1] for type in product_types]
    if product_type in product_types:
        products = ProductType.objects.get(product_type=product_type).products.all().order_by('product')
        signed_user = User.objects.filter(login=1).first()
        pic_name = f"{(product_type.lower()).replace(' ', '_')}.png"
        return render(request, 'product_page.html', {
            'products': products, 'signed_user': signed_user, 'pic_name': pic_name,
            'product_type': product_type, 'logo_name': generate_logo()})
    else:
        return render(request, '404.html')
