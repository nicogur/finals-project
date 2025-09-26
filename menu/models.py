from django.db import models
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Dish(models.Model):
    SPICE_CHOICES = [(i, str(i)) for i in range(5)]  # 0..4

    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='dishes')
    image = models.ImageField(upload_to='dishes/', blank=True, null=True)
    spiciness = models.IntegerField(choices=SPICE_CHOICES, default=0)
    has_nuts = models.BooleanField(default=False)
    vegetarian = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name



