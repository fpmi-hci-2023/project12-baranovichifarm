from rest_framework import serializers, renderers
from Farm.models import *


class stove_serializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        product = models.CharField(max_length=255, default=None)
        price = models.FloatField()
        information = models.CharField(max_length=255, default='Product from A.O Farm')
        fields = ('product', 'price', 'information')



