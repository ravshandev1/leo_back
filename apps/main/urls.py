from django.urls import path
from . import views

urlpatterns = [
    path('', views.WorkerAPI.as_view()),
    path('brands/', views.BrandAPI.as_view()),
    path('products/', views.ProductAPI.as_view()),
]
