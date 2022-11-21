from rest_framework.routers import DefaultRouter
from django.urls import path

from . import views

router = DefaultRouter()
router.register("", views.ProductViewSet, basename="product")

urlpatterns = [
    path("image/<int:pk>/", views.ProductImageRetrieve.as_view(), name="product_image")
]

urlpatterns += router.urls
