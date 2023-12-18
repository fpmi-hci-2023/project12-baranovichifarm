from django.shortcuts import render

from Farm.models import Product


def db_info(request):
    products = Product.objects.filter()
    return render(request, {'products': products})

