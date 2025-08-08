from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name


class Product(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_products')
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(category,on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.FloatField()
    rating = models.FloatField()
    stock = models.IntegerField()
    brand = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title