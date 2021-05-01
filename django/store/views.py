from django.shortcuts import render

from rest_framework import generics

from . import models
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductItemView(generics.RetrieveAPIView):
    lookup_field = 'slug'
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryListView(generics.ListAPIView):
    '''
    view the main categoris based on their hierarchy level
    '''
    queryset = Category.objects.filter(level=1)
    serializer_class = CategorySerializer


class CategoryItemView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        '''
        show all the items that has shoes in their categories
        '''
        return models.Product.objects.filter(category__in=Category.objects.get(slug=self.kwargs['slug']).get_descendants(include_self=True))
