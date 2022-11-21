from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView

from .models import Product, ProductImage
from .serializers import ProdcutSerializer, ProductImageSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProdcutSerializer
    http_method_names = ["get", "head", "patch", "delete"]
    lookup_field = "code"


class ProductImageRetrieve(RetrieveAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
