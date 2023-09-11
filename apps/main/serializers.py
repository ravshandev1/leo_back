from rest_framework import serializers
from .models import Worker, Brand, Product, Image


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['tele_id', 'username', 'first_name', 'last_name', 'phone']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image_path']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'images', 'description']

    images = ImageSerializer(many=True)
