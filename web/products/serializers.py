from rest_framework import serializers

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
    supply_date = serializers.DateField(format="%d.%m.%y")

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
