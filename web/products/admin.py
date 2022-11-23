from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from django.db.models import ImageField

from .models import Size, ProductImage, Product


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
    readonly_fields = ["code"]
    search_fields = ["name", "code"]
    
    @admin.display(description="Размеры")
    def sizes_range(self, obj):
        sizes = obj.sizes.all().order_by("value")
        return f"{sizes[0].value}-{sizes[len(sizes) - 1].value}"
