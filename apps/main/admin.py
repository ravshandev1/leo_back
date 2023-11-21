from django.contrib import admin
from .models import Worker, Brand, Category, Model, Image, Product, Cart, Order


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'count', 'is_ordered']
    list_filter = ['user', 'is_ordered']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    filter_horizontal = ['carts']
    list_display = ['id', 'user', 'is_done', 'created_at']
    list_filter = ['is_done', 'created_at']


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ['tele_id', 'phone', 'username', 'first_name', 'last_name', 'is_worker']
    search_fields = ['phone', 'first_name', 'last_name', 'username']
    list_filter = ['is_worker']


class ImageInline(admin.StackedInline):
    model = Image
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'model']
    inlines = [ImageInline]


class ModelInline(admin.StackedInline):
    model = Model
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_filter = ['brand']
    list_display = ['name', 'brand']
    inlines = [ModelInline]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
