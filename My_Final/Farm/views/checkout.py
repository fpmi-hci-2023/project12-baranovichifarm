from datetime import datetime
from django.conf import settings
from pytz import UTC
from django.core.mail import send_mail
from django.contrib import messages
from django.template import loader
from django.shortcuts import (render,
                              redirect, )
from My_Final.funcs import (generate_logo,
                       products_to_json,
                       get_superuser_email,
                       check_connection, )
from Farm.models import (User,
                               Basket,
                               Order, )
from Farm.forms import (CheckoutGuestForm,
                              CheckoutUserForm, )


def checkout(request):
    products = Basket.objects.filter().order_by('product')
    signed_user = User.objects.filter(login=1).first()
    products_costs = Basket.objects.filter().values_list('cost')
    products_costs = [cost[0] for cost in products_costs]
    order_total = round(sum(products_costs), 2)
    if signed_user:
        Form = CheckoutUserForm
        address = signed_user.address
    else:
        Form = CheckoutGuestForm
        address = None
    if request.method == 'GET':
        current_hour = datetime.now().hour
        if settings.CLOSING_HOUR > current_hour >= settings.OPENING_HOUR:
            return render(request, 'checkout_page.html', {
                'products': products, 'signed_user': signed_user, 'order_total': order_total,
                'logo_name': generate_logo(), 'form': Form(initial={'address': address})})
        else:
            return render(request, 'checkout_page.html', {
                'signed_user': signed_user, 'logo_name': generate_logo(), 'closed_status': True})
    elif request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            json_products = products_to_json(products)
            order_date = datetime.now(tz=UTC)
            if signed_user:
                Order.objects.create(
                    user_type='User',
                    first_name=signed_user.first_name,
                    last_name=signed_user.last_name,
                    email=signed_user.email,
                    phone_number=signed_user.phone_number,
                    address=data['address'],
                    order_date=order_date,
                    delivery_date=data['delivery_date'],
                    comment=data['comment'],
                    order_info=json_products,
                    user=signed_user, )
            else:
                Order.objects.create(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    phone_number=data['phone_number'],
                    address=data['address'],
                    order_date=order_date,
                    delivery_date=data['delivery_date'],
                    comment=data['comment'],
                    order_info=json_products, )
            admin_email = settings.ADMIN_EMAIL
            if not admin_email:
                admin_email = get_superuser_email()
            customer_email = signed_user.email if signed_user else data['email']
            order = Order.objects.filter(order_date=order_date).first()
            if check_connection():
                html_message = loader.render_to_string(
                    'email_message.html',
                    {'products': products, 'order_total': order_total, 'order': order}, )
                send_mail(
                    subject='Farm (A.O.)',
                    message='',
                    html_message=html_message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[customer_email, admin_email])
                messages.add_message(request, messages.SUCCESS,
                                     f'{order.first_name}, thank you for your order!')
                messages.add_message(request, messages.SUCCESS,
                                     'You will shortly receive a confirmation email.')
            else:
                messages.add_message(request, messages.SUCCESS,
                                     f'{order.first_name}, thank you for your order!')
                messages.add_message(request, messages.INFO,
                                     'Cannot send a confirmation email. Check your internet connection.')
            Basket.objects.all().delete()
            return redirect('home_page')
        return render(request, 'checkout_page.html', {
            'products': products, 'signed_user': signed_user, 'order_total': order_total,
            'logo_name': generate_logo(), 'form': form})
