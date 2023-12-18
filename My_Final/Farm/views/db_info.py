from My_Final.funcs import generate_logo
from django.shortcuts import (render,
                              redirect, )
from Farm.models import (User,
                               Order, )


def db_info(request):
    users = User.objects.filter()
    orders = Order.objects.filter()
    return render(request, 'db_info.html', {'users': users, 'orders': orders, 'logo_name': generate_logo()})


def delete_from_user(request, user_id):
    user = User.objects.filter(id=user_id).first()
    if user:
        user.delete()
        return redirect('bd_info')
    else:
        return render(request, '404.html')


def delete_from_order(request, order_id):
    order = Order.objects.filter(id=order_id).first()
    if order:
        order.delete()
        return redirect('bd_info')
    else:
        return render(request, '404.html')
