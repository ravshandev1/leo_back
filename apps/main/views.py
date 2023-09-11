from rest_framework import generics, response, status
from .serializers import WorkerSerializer, ProductSerializer, BrandSerializer
from .models import Worker, Brand, Product


class WorkerAPI(generics.CreateAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

    def get(self, request, *args, **kwargs):
        tele_id = self.request.query_params.get('id')
        user = Worker.objects.filter(tele_id=tele_id).first()
        if user is not None:
            if user.is_worker is False:
                return response.Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            return response.Response()
        else:
            return response.Response(status=status.HTTP_404_NOT_FOUND)


class BrandAPI(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ProductAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        brand = Brand.objects.filter(name__exact=self.request.query_params.get('br')).first()
        qs = self.queryset.filter(brand=brand, name__iexact=self.request.query_params.get('name')).first()
        if qs:
            serializer = self.get_serializer(qs)
            return response.Response(serializer.data)
        else:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
