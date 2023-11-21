from rest_framework import generics, response, status, views
from .serializers import WorkerSerializer, CategorySerializer, ModelSerializer, BrandSerializer, ImageSerializer, \
    ProductSerializer
from .models import Worker, Brand, Category, Model, Image, Product, Cart, Order
import requests
from django.conf import settings


class WorkerAPI(generics.CreateAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

    def get(self, request, *args, **kwargs):
        tele_id = self.request.query_params.get('id')
        user = Worker.objects.filter(tele_id=tele_id).first()
        if user:
            if user.is_worker is False:
                return response.Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            return response.Response()
        else:
            return response.Response(status=status.HTTP_404_NOT_FOUND)


class BrandAPI(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CategoryAPI(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        brand = Brand.objects.filter(name__exact=self.request.query_params.get('brand')).first()
        return Category.objects.filter(brand=brand)


class ModelAPI(generics.ListAPIView):
    serializer_class = ModelSerializer

    def get_queryset(self):
        brand = Brand.objects.filter(name__exact=self.request.query_params.get('brand')).first()
        category = Category.objects.filter(name__exact=self.request.query_params.get('category'), brand=brand).first()
        return Model.objects.filter(category=category)


class ProductAPI(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        brand = Brand.objects.filter(name__exact=self.request.query_params.get('brand')).first()
        category = Category.objects.filter(name__exact=self.request.query_params.get('category'), brand=brand).first()
        model = Model.objects.filter(name__exact=self.request.query_params.get('model'), category=category).first()
        return Product.objects.filter(model=model)


class ImageAPI(views.APIView):

    def get(self, request, *args, **kwargs):
        qs = Image.objects.filter(product__name__exact=self.request.query_params.get('product'))
        serializer = ImageSerializer(qs, many=True)
        return response.Response(serializer.data)


class ProductDetailAPI(views.APIView):

    def get(self, request, *args, **kwargs):
        qs = Product.objects.filter(name__exact=self.request.query_params.get('product')).first()
        serializer = ProductSerializer(qs)
        return response.Response(serializer.data)


class MyCartAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        qs = Cart.objects.filter(user__tele_id=self.kwargs.get('tele_id'), is_ordered=False)
        summa = 0
        ls = list()
        for i in qs:
            ls.append({'product': i.product.name, 'count': i.count, 'total_price': i.total_price})
            summa += i.total_price
        return response.Response({'total_price': summa, 'results': ls})

    def put(self, request, *args, **kwargs):
        qs = Cart.objects.filter(user__tele_id=self.kwargs.get('tele_id'), is_ordered=False)
        if qs:
            user = Worker.objects.filter(tele_id=self.kwargs.get('tele_id')).first()
            order = Order.objects.create(user_id=user.id)
            txt = f"Mijoz: <b>{user.first_name}</b>\n"
            txt += f"Telefon raqam: <b>{user.phone}</b>\n"
            txt += f"Buyurtma raqami: <b>{order.id}</b>\n"
            summa = 0
            for i in Cart.objects.filter(user__tele_id=self.kwargs.get('tele_id'), is_ordered=False):
                txt += f"Product: <b>{i.product.name}</b> dan <b>{i.count}</b> ta\n"
                summa += i.total_price
                i.is_ordered = True
                i.save()
                order.carts.add(i)
            txt += f"Jami: <b>{summa}$</b>\n"
            txt += f"Buyurtma vaqti: <b>{order.created_at.__format__('%-m/%d/%Y, %H:%M')}</b>"
            requests.get(url=f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendmessage",
                         params={'chat_id': '-4096787100', 'text': txt, 'parse_mode': 'HTML'})
        return response.Response()

    def post(self, request, *args, **kwargs):
        worker = Worker.objects.filter(tele_id=self.kwargs.get('tele_id')).first()
        product = Product.objects.filter(name__exact=self.request.data['product']).first()
        Cart.objects.create(user_id=worker.id, product_id=product.id, count=self.request.data['count'])
        return response.Response()

    def delete(self, request, *args, **kwargs):
        for i in Cart.objects.filter(user__tele_id=self.kwargs.get('tele_id'), is_ordered=False):
            i.delete()
        return response.Response()
