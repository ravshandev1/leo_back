import json
import requests
from django.db import models
from django.conf import settings


class Brand(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Category(models.Model):
    brand = models.ForeignKey(Brand, models.CASCADE, related_name='categories')
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Model(models.Model):
    category = models.ForeignKey(Category, models.CASCADE, related_name='models')
    name = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.name} {self.category.name} {self.category.brand.name}"


class Product(models.Model):
    model = models.ForeignKey(Model, models.CASCADE, related_name='products')
    name = models.CharField(max_length=250, unique=True)
    price = models.PositiveBigIntegerField(default=1)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(Product, models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products')

    def __str__(self):
        return self.product.name

    @property
    def image_path(self):
        return f"http://95.130.227.254{self.image.url}"


class Worker(models.Model):
    tele_id = models.PositiveIntegerField(unique=True)
    phone = models.CharField(max_length=250)
    username = models.CharField(max_length=250, null=True, blank=True)
    first_name = models.CharField(max_length=250, null=True, blank=True)
    last_name = models.CharField(max_length=250, null=True, blank=True)
    is_worker = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.phone}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.is_worker:
            requests.get(url=f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendmessage",
                         params={'chat_id': self.tele_id,
                                 'text': "Sizga Admin tomonidan botdan foydalanishga ruxsat berildi!!!",
                                 'reply_markup': json.dumps(
                                     {"keyboard": [[{"text": "Brandlar"}, {"text": "Savatcham"}]],
                                      "resize_keyboard": True})})
        super().save()


class Cart(models.Model):
    user = models.ForeignKey(Worker, models.CASCADE, related_name='carts')
    product = models.ForeignKey(Product, models.CASCADE, related_name='carts')
    count = models.PositiveBigIntegerField(default=1)
    is_ordered = models.BooleanField(default=False)

    @property
    def total_price(self):
        return self.product.price * self.count

    def __str__(self):
        return f"{self.product.name} - ({self.count}) ta"


class Order(models.Model):
    user = models.ForeignKey(Worker, models.CASCADE, related_name='orders')
    carts = models.ManyToManyField(Cart, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.user.phone
