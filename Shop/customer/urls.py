from django.urls import path
from customer.views import *

urlpatterns = [
    path('add/', customer, name='add_customer'),
    path('update/', customer, name='update_customer'),
    path('delete/', customer, name='delete_customer')
]
