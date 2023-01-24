from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("", views.ProductViewSet, basename="product")

urlpatterns = [
    path("image/<int:pk>/", views.ProductImageRetrieve.as_view(), name="product_image"),
    path("commit_sold/<str:product_code>/", views.ProductSoldView.as_view(), name="commit_sold"),
    path("commit_sold/pack/<str:product_code>/", views.ProductSoldPackView.as_view(), name="commit_sold_pack"),
]

urlpatterns += router.urls
