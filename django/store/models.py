from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from model_utils.models import TimeStampedModel


class Category(MPTTModel):
    name = models.CharField(
        verbose_name=_('Category Name'),
        help_text=_('Unique and Required'),
        max_length=255,
        unique=True
    )
    slug = models.SlugField(
        verbose_name=_('Category Safe URL'),
        max_length=255,
        unique=True
    )
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name="children")
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _("Categories")

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(verbose_name=_(
        'Product Name'), help_text=_('Required'), max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Product Type')
        verbose_name_plural = _('Product Types')

    def __str__(self):
        return self.name


class ProductSpec(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    name = models.CharField(verbose_name=_(
        'Name'), help_text=_('Required'), max_length=255)

    class Meta:
        verbose_name = _('Product Specification')
        verbose_name_plural = _('product Specifications')

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    title = models.CharField(
        verbose_name=_('title'),
        help_text=_('Required'),
        max_length=255
    )
    description = models.TextField(verbose_name=_(
        'Description'), help_text=_('Not Required'), blank=True)
    slug = models.SlugField(max_length=255)
    regular_price = models.DecimalField(
        verbose_name=_('Regular Price'),
        help_text=_('Max 99.99'),
        error_messages={
            'name': {
                'max_length': _('The price must be between 0-99.99')
            }
        },
        max_digits=4,
        decimal_places=2
    )
    discount_price = models.DecimalField(
        verbose_name=_('Discount Price'),
        help_text=_('Max 99.99'),
        error_messages={
            'name': {
                'max_length': _('The price must be between 0-99.99')
            }
        },
        max_digits=4,
        decimal_places=2
    )
    is_active = models.BooleanField(
        verbose_name=_('Product Visibility'),
        help_text=_('Change product visibility'),
        default=True)

    class Meta:
        ordering = ('-created')
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def get_absolute_url(self):
        return reverse("store:product_detail", kwargs={"pk": self.pk},
                       args=[self.slug])

    def __str__(self):
        return self.title


class ProductSpecValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    spec = models.ForeignKey(ProductSpec, on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_('value'),
        help_text=_('Product Specification value'),
        max_length=255
    )

    class Meta:
        verbose_name = _('Product Specification Value')
        verbose_name_plural = _('product Specification Values')

    def __str__(self):
        return self.value


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_image')
    image = models.ImageField(
        verbose_name=_('image'),
        help_text=_('Upload a product image'),
        upload_to='images/',
        default='images/default.png',
    )
    alt_text = models.CharField(
        verbose_name=_('alternative text'),
        help_text=_('please add an alter text'),
        max_length=255,
        null=True,
        blank=True,
    )
    is_feature = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')
