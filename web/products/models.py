import uuid
from typing import Type

from django.db import models


def get_upload_path(instance: Type[models.Model], filename: str) -> str:
    """Construct image path"""
    return filename


def generate_uid() -> str:
    return uuid.uuid1().hex[:7].upper()


class Product(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название")
    code = models.CharField(default=generate_uid, unique=True, max_length=7, verbose_name="Артикул")
    color = models.CharField(max_length=50, verbose_name="Цвет")
    quantity = models.BigIntegerField(verbose_name="Количество товара")
    pack_quantity = models.BigIntegerField(verbose_name="Количество пачек")
    wholesale_price = models.IntegerField(verbose_name="Оптовая Цена")
    retail_price = models.IntegerField(verbose_name="Розничная Цена")
    sold = models.BigIntegerField(verbose_name="Продано")
    remainder = models.BigIntegerField(verbose_name="Остаток")
    defective = models.BigIntegerField(verbose_name="Брак")
    refund = models.BigIntegerField(verbose_name="Возврат")
    supply_date = models.DateField(verbose_name="Дата поставки")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self) -> str:
        return f"{self.name[:50]}: {self.code}"


class Size(models.Model):
    value = models.IntegerField(verbose_name="Размер")
    quantity = models.BigIntegerField(verbose_name="Количество")
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="sizes")

    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"

    def __str__(self) -> str:
        return str(self.value)


class ProductImage(models.Model):
    image = models.ImageField(upload_to=get_upload_path)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фотографии"

    def __str__(self) -> str:
        return f"{self.product.name[:50]}"
