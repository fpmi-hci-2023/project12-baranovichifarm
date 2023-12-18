from django.shortcuts import render, redirect
from django.template import loader
from django.http.response import HttpResponse
from customer.models import Customer


def customer(request):
    if request.method == "GET":
        if request.path == "/customer/add":
            context = {"type": "Add", "url": "add"}
        elif request.path == "/customer/update":
            context = {"type": "Update", "url": "update"}
        else:
            context = {"type": "Delete", "url": "delete"}
        template = loader.get_template('customer.html')
        return HttpResponse(template.render(context, request))
    elif request.method == "POST":
        data = request.POST
        email = data.get("email")
        password = data.get("password")
        if request.path == "/customer/add":
            customer = Customer(email=email, password=password)
        elif request.path == "/customer/update":
            customer = Customer.objects.get(email=email)
        else:
            Customer.objects.get(email=email).delete()
            return redirect('/home/')
        customer.email = email
        customer.password = password
        try:
            customer.save()
        except Exception as err:
            print(err)
            return HttpResponse(status=409)
        return redirect('/home/')
