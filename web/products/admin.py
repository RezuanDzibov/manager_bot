from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from django.db.models import ImageField

from .models import Color, Size, ProductImage, Product


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


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    pass


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    formfield_overrides = {
        ImageField: {"widget": ProdcutImageWidget}
    }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
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
    )
    list_filter = ("color", "size", "refund", "defective")
    list_display_links = ("name", "color", "size")
    inlines = [ProductImageInline]
    readonly_fields = ["code"]
    search_fields = ["name", "code"]
