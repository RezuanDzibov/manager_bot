from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveAPIView, GenericAPIView
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from . import services
from .models import Product, ProductImage
from .serializers import ProductSerializer, ProductImageSerializer, SoldCommitSerializer, ProductAddSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ["get", "head", "patch", "delete"]
    lookup_field = "code"


class ProductImageRetrieve(RetrieveAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class ProuductSoldView(GenericAPIView):
    serializer_class = SoldCommitSerializer

    @swagger_auto_schema()
    def patch(self, request: HttpRequest, product_code: str) -> Response:
        sold = services.commit_sold(
            product_code=product_code,
            size=int(request.data["size"]),
            quantity=int(request.data["quantity"])
        )
        return Response(status=200, data=sold)


class ProductCreateView(GenericAPIView):
    serializer_class = ProductAddSerializer

    @swagger_auto_schema(responses={201: ProductSerializer()})
    def post(self, request: HttpRequest) -> Response:
        product = services.create_product(data=request.data.copy())
        return Response(status=201, data=ProductSerializer(product).data)


class ProductImageAddView(APIView):
    @swagger_auto_schema()
    def post(self, request: HttpRequest, code: str) -> Response:
        services.add_image_to_product(product_code=code, data=request.data.copy())
        return Response(status=201)
