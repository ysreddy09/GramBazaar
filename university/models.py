from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    roles = models.CharField(max_length=20,
                             choices=(('Admin', 'Admin'), ('Seller', 'Seller'), ('Customer', 'Customer')))
    is_verified = models.BooleanField(default=False)


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.AutoField(primary_key=True)
    product_image = models.ImageField(upload_to='product_images/')
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0,
                                         validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])


class PurchaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchased_datetime = models.DateTimeField(auto_now_add=True)
    seller_name = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255)
