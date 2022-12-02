from pathlib import Path

from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

from .models import Product, ProductImage, Size


class ProductImageListField(serializers.RelatedField):
    def to_representation(self, obj) -> str:
        return obj.image.url


class SizeListField(serializers.RelatedField):
    def to_representation(self, obj: Size) -> dict:
        return {
            "size_value": obj.value,
            "size_quantity": obj.quantity,
        }



class ProductSerializer(serializers.ModelSerializer):
    sizes = SizeListField(many=True, read_only=True)
    images = ProductImageListField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "code",
            "color",
            "quantity",
            "pack_quantity",
            "wholesale_price",
            "retail_price",
            "supply_date",
            "sold",
            "remainder",
            "defective",
            "refund",
            "sizes",
            "images",
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image"]


class SoldCommitSerializer(serializers.Serializer):
    size = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)


class SizeAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        exclude = ["product"]


class ProductAddSerializer(serializers.ModelSerializer):
    sizes = SizeAddSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "name",
            "color",
            "quantity",
            "pack_quantity",
            "wholesale_price",
            "retail_price",
            "supply_date",
            "sold",
            "remainder",
            "defective",
            "refund",
            "sizes",
        ]


class ProductImageExtensionValidator(FileExtensionValidator):
    def __call__(self, value):
        extension = Path(value).suffix[1:].lower()
        if (
            self.allowed_extensions is not None
            and extension not in self.allowed_extensions
        ):
            raise ValidationError(
                self.message,
                code=self.code,
                params={
                    "extension": extension,
                    "allowed_extensions": ", ".join(self.allowed_extensions),
                    "value": value,
                },
            )


class ProductImageAddFiled(serializers.CharField):
    default_error_messages = {
        "invalid": "Not a valid image path.",
        "blank": "This field may not be blank.",
        "max_length": "Ensure this field has no more than {max_length} characters.",
        "min_length": "Ensure this field has at least {min_length} characters.",
        "image_extension": "Ensure this field has extension jpg or png"
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators.append(ProductImageExtensionValidator(["png", "jpg"]))


class ProductImageAddSerializer(serializers.Serializer):
    images = serializers.ListSerializer(child=ProductImageAddFiled())

    class Meta:
        model = ProductImage
        fields = ["images"]
