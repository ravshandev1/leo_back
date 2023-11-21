from django.urls import path
from . import views

urlpatterns = [
    path('', views.WorkerAPI.as_view()),
    path('brands/', views.BrandAPI.as_view()),
    path('categories/', views.CategoryAPI.as_view()),
    path('models/', views.ModelAPI.as_view()),
    path('products/', views.ProductAPI.as_view()),
    path('images/', views.ImageAPI.as_view()),
    path('product-detail/', views.ProductDetailAPI.as_view()),
    path('my-cart/<int:tele_id>/', views.MyCartAPI.as_view()),
]
