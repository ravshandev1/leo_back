from rest_framework import serializers
from .models import Worker, Brand, Category, Model, Image, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description']


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['tele_id', 'username', 'first_name', 'last_name', 'phone']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ['name']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image_path']
