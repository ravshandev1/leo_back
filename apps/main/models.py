import requests
from django.db import models
from django.conf import settings


class Brand(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=250)
    brand = models.ForeignKey(Brand, models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(Product, models.CASCADE, related_name='images')
    image = models.FileField(upload_to='products')

    def __str__(self):
        return self.product.name

    @property
    def image_path(self):
        return f"{self.image.path}"


class Worker(models.Model):
    tele_id = models.PositiveIntegerField(unique=True)
    phone = models.CharField(max_length=250)
    username = models.CharField(max_length=250, null=True, blank=True)
    first_name = models.CharField(max_length=250, null=True, blank=True)
    last_name = models.CharField(max_length=250, null=True, blank=True)
    is_worker = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tele_id} {self.username}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.is_worker:
            requests.get(url=f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendmessage",
                         params={
                             'text': "Sizga Admin tomonidan botdan foydalanishga ruxsat berildi!!!\n/help kamandasini bosing!!",
                             'chat_id': self.tele_id})

        super().save()
