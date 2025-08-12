from django.db import models
from cloudinary.models import CloudinaryField
# Create your models here.


from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name


class Supplier(models.Model):
    supplier_name = models.CharField(max_length=100, unique=True)
    contact_email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.supplier_name



class Product(models.Model):
    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=15.00)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    image = CloudinaryField('image', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    suppliers = models.ManyToManyField(Supplier,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
