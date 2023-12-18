from django.contrib import admin
from Farm.models import (ProductType,
                               Product,)


admin.site.register(ProductType)
admin.site.register(Product)
