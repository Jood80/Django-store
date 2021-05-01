from django.shortcuts import render

from rest_framework import generics

from . import models
from .models import Product, Category
from .serializers import ProductSerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductItemView(generics.RetrieveAPIView):
    lookup_field = 'slug'
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryItemView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return models.Product.objects.filter(category__slug=self.kwargs['slug'])
