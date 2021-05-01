from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import(
    Category,
    Product,
    ProductSpec,
    ProductSpecValue,
    ProductType,
    ProductImage,
)

admin.site.register(Category, MPTTModelAdmin)


class ProductSpecInline(admin.TabularInline):
    model = ProductSpec


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductSpecValueInline(admin.TabularInline):
    model = ProductSpecValue


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecInline,
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecValueInline,
        ProductImageInline,
    ]
