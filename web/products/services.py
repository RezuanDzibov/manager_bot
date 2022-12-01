from django.db import IntegrityError
from django.db import transaction
from django.db.models import F
from rest_framework.exceptions import NotFound, ValidationError

from .models import Product, Size, ProductImage
from .serializers import ProdcutAddSerializer, ProductImageAddSerializer


def commit_sold(product_code: str, size: int, quantity: int) -> dict:
    try:
        product = Product.objects.get(code=product_code)
    except Product.DoesNotExist:
        raise NotFound("Product doesn't exists")
    try:
        size = Size.objects.get(product=product, value=size)
    except Size.DoesNotExist:
        raise NotFound("Size doesn't exists")
    size_initial_quantity = size.quantity
    try:
        with transaction.atomic():
            size.quantity = F("quantity") - quantity
            size.save()
            product.remainder = F("remainder") - quantity
            product.sold = F("sold") + quantity
            product.save()
        product.refresh_from_db()
        size.refresh_from_db()
        return {
            "name": product.name,
            "code": product.code,
            "quantity": product.quantity,
            "sold": product.sold,
            "remainder": product.remainder,
            "sizes": list([{"size_value": size.value, "size_quantity": size.quantity} for size in product.sizes.all()])

        }
    except IntegrityError:
        raise ValidationError(
            {
                "client_quantity": quantity,
                "initial_quantity": size_initial_quantity,
                "size": size.value,
                "product_name": product.name
            },
            code=400
        )


def create_product(data: dict):
    serializer = ProdcutAddSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    sizes_data = data.pop("sizes")
    with transaction.atomic():
        product = Product.objects.create(**data)
        sizes = [Size(product=product, **size_data) for size_data in sizes_data]
        Size.objects.bulk_create(sizes)
        return product


def add_image_to_product(product_code: str, data: dict):
    serializer = ProductImageAddSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    try:
        product = Product.objects.get(code=product_code)
    except Product.DoesNotExist:
        raise NotFound("Product doesn't exists")
    images = [ProductImage(product=product, image=image) for image in data["images"]]
    ProductImage.objects.bulk_create(images)
