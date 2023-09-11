from django.contrib import admin
from .models import Worker, Brand, Product, Image


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ['tele_id', 'phone', 'username', 'first_name', 'last_name', 'is_worker']
    search_fields = ['phone', 'first_name', 'last_name', 'username']
    list_filter = ['is_worker']


class ImageInline(admin.StackedInline):
    model = Image
    extra = 0


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['brand']
    inlines = [ImageInline]
