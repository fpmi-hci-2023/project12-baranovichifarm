from django.contrib import messages
from django.shortcuts import (render,
                              redirect, )
from Farm.models import (Product,
                               User,
                               Basket, )


def add_to_basket(request, product_id):
    products = Product.objects.filter().values_list('id')
    products = [product[0] for product in products]
    if not int(product_id) in products:
        return render(request, '404.html')
    product_in_order = Basket.objects.filter(product_id=product_id).first()
    product_to_order = Product.objects.get(id=product_id)
    product_amount = int(request.POST.get('amount'))
    product_type = product_to_order.type
    referer = request.META['HTTP_REFERER']
    inclusion = 'checkout' in referer
    if product_amount or inclusion:
        if not product_amount:
            Basket.objects.filter(product_id=product_id).delete()
        elif product_in_order:
            Basket.objects.filter(product_id=product_id).update(
                amount=product_amount,
                cost=product_amount * product_to_order.price)
            if not inclusion:
                messages.add_message(request, messages.SUCCESS,
                                     f'The amount of "{product_to_order.product}" in your cart has been successfully '
                                     f'changed to {int(product_amount)} pcs.')
        else:
            Basket.objects.create(
                product_id=product_id,
                product_type=product_to_order.type,
                product=product_to_order.product,
                price=product_to_order.price,
                amount=product_amount,
                cost=product_amount * product_to_order.price, )
            messages.add_message(request, messages.SUCCESS,
                                 f'{int(product_amount)} pcs. of "{product_to_order.product}" '
                                 f'has been successfully added to your cart.')
    if inclusion:
        return redirect('checkout')
    return redirect('product_page', product_type=product_type)


def delete_from_basket(request, product_id):
    product = Basket.objects.filter(product_id=product_id).first()
    if product:
        product.delete()
        return redirect('checkout')
    else:
        return render(request, '404.html')
