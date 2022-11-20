import uuid
from typing import Type

from django.db import models


def get_upload_path(instance: Type[models.Model], filename: str) -> str:
    """Construct image path"""
    return filename


def generate_uid() -> str:
    return uuid.uuid1().hex[:7].upper()


class Size(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Size"
        verbose_name_plural = "Sizes"

    def __str__(self) -> str:
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colors"

    def __str__(self) -> str:
        return self.name


class ProductImage(models.Model):
    alt_text = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to=get_upload_path)
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="images")

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def __str__(self) -> str:
        return f"{self.product.name} {self.alt_text}"


class Product(models.Model):
    name = models.CharField(max_length=500)
    code = models.CharField(default=generate_uid, unique=True, max_length=6)
    available = models.BooleanField(default=True)
    quantity = models.BigIntegerField()
    size = models.ForeignKey(Size, on_delete=models.PROTECT)
    color = models.ForeignKey(Color, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self) -> str:
        return self.name[:50]
