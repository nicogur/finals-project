from django.contrib import admin
from .models import Category, Dish

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'spiciness', 'has_nuts', 'vegetarian', 'price')
    list_filter = ('category', 'spiciness', 'has_nuts', 'vegetarian')
    search_fields = ('name', 'description')

