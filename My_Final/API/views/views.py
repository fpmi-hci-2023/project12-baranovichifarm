from django.shortcuts import render
from rest_framework.views import APIView
from Farm.models import *
from API.serializer import stove_serializer
from rest_framework.response import Response


class GetStoveInfoView(APIView):
    def get(self, request):
        queryset = Product.objects.all()
        serializer_for_queryset = stove_serializer(
            instance=queryset,
            many=True
        )
        return Response(serializer_for_queryset.data)



class ProductView(APIView):
    def post(self, request):
        serializer = stove_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
