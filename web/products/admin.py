from datetime import datetime
from io import StringIO

from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.db.models import ImageField
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from .models import Size, ProductImage, Product, Order, Customer


class ProdcutImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(
                f'<a href="{image_url}" target="_blank">'
                f'<img src="{image_url}" alt="{file_name}" width="300" height="300" '
                f'style="object-fit: cover;"/> </a>')

        output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))
        return mark_safe(u"".join(output))


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    formfield_overrides = {
        ImageField: {"widget": ProdcutImageWidget}
    }


class SizeInline(admin.TabularInline):
    model = Size


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "color",
        "quantity",
        "pack_quantity",
        "wholesale_price",
        "retail_price",
        "sizes_range",
        "sold",
        "remainder",
        "defective",
        "refund",
        "supply_date",
    )
    list_display_links = ("name",)
    inlines = [SizeInline, ProductImageInline]
    search_fields = ["name", "code"]
    actions = ["download_product_list"]

    @admin.display(description="Размеры")
    def sizes_range(self, obj):
        sizes = obj.sizes.all().order_by("value")
        if len(sizes) > 1:
            return f"{sizes[0].value}-{sizes[len(sizes) - 1].value}"
        return sizes[0].value

    @admin.action(description="Скачать артикулы")
    def download_product_list(self, request, queryset):
        products = list()
        for product in queryset:
            sizes = product.sizes.all().order_by("value")
            if len(sizes) > 1:
                sizes_range = f"{sizes[0].value}-{sizes[len(sizes) - 1].value}"
            else:
                sizes_range = str(sizes[0].value)
            products.append(f"Название: {product.name}\nАртикул: {product.code}\nРазмеры: {sizes_range}")
        file = StringIO()
        file.write("\n\n".join(products))
        file.seek(0)
        response = HttpResponse(file, content_type="text")
        response["Content-Disposition"] = f"attachment; filename=Products from {str(datetime.now().strftime('%m.%d.%y at %H.%M.%S'))}.txt"
        return response


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["__str__", "is_paid", "quantity", "product_price", "sum", "is_debt", "pay_date"]
    readonly_fields = ["product_price", "sum", "is_paid"]

    @admin.display(description="Оплачен")
    def is_paid(self, obj: Order):
        if obj.is_paid:
            return "Да"
        return "Нет"

    @admin.display(description="Стоимость товара")
    def product_price(self, obj: Order):
        return obj.product_price

    @admin.display(description="Сумма")
    def sum(self, obj: Order):
        return obj.product_price * obj.quantity


class OrderInline(admin.TabularInline):
    model = Order


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    inlines = [OrderInline]
