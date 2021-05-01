from rest_framework import serializers

from .models import Product, ProductImage


class ImageSerilizer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text']


class ProductSerializer(serializers.ModelSerializer):
    product_image = ImageSerilizer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description',
                  'slug', 'regular_price', 'product_image']
