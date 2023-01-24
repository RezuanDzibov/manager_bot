from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveAPIView, GenericAPIView
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from . import services
from .models import Product, ProductImage
from .serializers import ProductSerializer, ProductImageSerializer, SoldCommitSerializer


class ProductViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ["get", "head", "patch"]
    lookup_field = "code"


class ProductImageRetrieve(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class ProductSoldView(GenericAPIView):
    serializer_class = SoldCommitSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema()
    def patch(self, request: HttpRequest, product_code: str) -> Response:
        sold = services.commit_sold(
            product_code=product_code,
            size=int(request.data["size"]),
            quantity=int(request.data["quantity"])
        )
        return Response(status=200, data=sold)


class ProductSoldPackView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SoldCommitSerializer

    @swagger_auto_schema()
    def patch(self, request: HttpRequest, product_code: str) -> Response:
        product = services.commit_sold_pack(product_code=product_code)
        return Response(status=200, data=product)
