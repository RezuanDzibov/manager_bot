from rest_framework import serializers

from .models import Product, ProductImage


class ProductImageListField(serializers.RelatedField):
    def to_representation(self, value) -> str:
        return value.image.url


class ProdcutSerializer(serializers.ModelSerializer):
    color = serializers.CharField(source="color.name")
    size = serializers.CharField(source="size.name")
    images = ProductImageListField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "code",
            "quantity",
            "remainder",
            "defective",
            "color",
            "size",
            "wholesale_price",
            "retail_price",
            "supply_date",
            "sale_date",
            "refund",
            "images",
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["alt_text", "image"]
